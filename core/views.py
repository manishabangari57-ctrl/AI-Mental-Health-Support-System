from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from mood.models import Mood
from mental_assessment.models import Assessment
from mental_assessment.forms import AssessmentForm
from core.ml_model import predict_risk, get_recommendation, train_model
from .models import Profile
from .forms import ProfileForm
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# -------------------- HOME --------------------
def home(request):
    return render(request, 'home.html')


# -------------------- SIGNUP --------------------
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/accounts/login/')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})


# -------------------- MOOD TRACKER --------------------
@login_required(login_url='accounts/login')
def mood(request):
    if request.method == "POST":
        mood_value = request.POST.get("mood")
        note = request.POST.get("note")
      
        # 🔥 VADER Sentiment Analysis
        analyzer = SentimentIntensityAnalyzer()

        sentiment = "neutral"
        if note:
         score = analyzer.polarity_scores(note)
         compound = score['compound']

         if compound > 0.05:
          sentiment = "positive"
         elif compound < -0.05:
          sentiment = "negative"

        Mood.objects.create(
            user=request.user,
            mood=mood_value,
            note=note,
            sentiment=sentiment
        )

        return redirect("mood")
    today = timezone.now()
    seven_days_ago = today - timedelta(days=7)
    moods = Mood.objects.filter(user=request.user,date__gte=seven_days_ago).order_by("-date")

    return render(request, 'mood.html', {"moods": moods})


# -------------------- MOOD HISTORY --------------------

def mood_history(request):
    moods = Mood.objects.filter(user=request.user).order_by("date")

    dates = []
    mood_values = []

    mood_map = {
        "happy": 5,
        "excited": 5,
        "calm": 4,
        "neutral": 3,
        "tired": 2,
        "sad": 2,
        "stressed": 1,
        "angry": 1,
        "anxious": 1
    }
    
    for mood in moods:
        dates.append(mood.date.strftime("%Y-%m-%d"))
        mood_values.append(mood_map.get(mood.mood, 3))

    return render(request, "mood_history.html", {
        "dates": dates,
        "moods": mood_values,

    })




# -------------------- AI MOOD PAGE --------------------

@login_required(login_url='/accounts/login/')
def ai_mood(request):
    from django.utils import timezone
    from datetime import timedelta

    last_week = timezone.now() - timedelta(days=7)

    moods = Mood.objects.filter(
        user=request.user,
        date__gte=last_week
    ).order_by("date")

    mood_map = {
        "angry": 1,
        "sad": 2,
        "neutral": 3,
        "happy": 4
    }

    mood_values = [mood_map.get(m.mood, 3) for m in moods]

    avg_mood = round(sum(mood_values) / len(mood_values), 2) if moods else 0
    negative_count = sum(1 for m in moods if m.mood in ["sad", "angry"])
    negative_sentiment = sum(1 for m in moods if m.sentiment == "negative")

    latest = moods.last() if moods else None
    latest_mood = latest.mood.lower() if latest else None
    latest_sentiment = latest.sentiment if latest else None

    # SENTIMENT SCORE
    avg_sentiment = (
        sum(
            1 if m.sentiment == "positive"
            else -1 if m.sentiment == "negative"
            else 0
            for m in moods
        ) / len(moods)
        if moods else 0
    )

    # TREND
    trend = "stable"
    if len(mood_values) >= 4:
        last3 = mood_values[-3:]
        prev = mood_values[:-3]

        if prev:
            if sum(last3)/3 - sum(prev)/len(prev) > 0.3:
                trend = "improving"
            elif sum(prev)/len(prev) - sum(last3)/3 > 0.3:
                trend = "declining"

    # ASSESSMENT
    latest_assessment = Assessment.objects.filter(
        user=request.user
    ).order_by('-date').first()

    assessment_level = latest_assessment.level.lower() if latest_assessment else None

    # PROFILE
    profile = Profile.objects.filter(user=request.user).first()
    user_concern = profile.concern if profile else None
    user_age = profile.age if profile else None

    # ------------------ RISK ------------------
    risk = "Moderate"

    if avg_mood <= 2 or negative_count >= 4 or avg_sentiment < -0.5:
        risk = "High"
    elif avg_mood >= 3.2 and avg_sentiment >= 0:
        risk = "Low"

    # assessment override
    if assessment_level == "high":
        risk = "High"
    elif assessment_level == "moderate" and risk == "Low":
        risk = "Moderate"

    # current positive override
    if latest_mood == "happy" and latest_sentiment == "positive":
        if risk == "High":
            risk = "Moderate"

    # ------------------ INSIGHT ------------------
    if not moods:
        insight = "Start tracking your mood to unlock insights."
    else:
        # base
        if avg_mood >= 3.5:
            insight = "You’ve been feeling positive most of the week 😊"
        elif avg_mood >= 2.5:
            insight = "Your mood has been mostly balanced this week 🙂"
        else:
            insight = "You’ve been experiencing low moods recently 😔"

        # trend
        if trend == "improving":
            insight += " and your mood is improving 📈."
        elif trend == "declining":
            insight += " and your mood is declining 📉."
        else:
            insight += " with a stable pattern ➖."

        # sentiment merge
        if latest_sentiment == "positive":
            insight += " Your recent thoughts are positive."
        elif latest_sentiment == "negative":
            insight += " Your recent thoughts show negativity."

        # mismatch
        if latest_mood == "happy" and latest_sentiment == "negative":
            insight += " Even though you feel happy, your thoughts suggest stress."
        elif latest_mood in ["sad", "angry"] and latest_sentiment == "positive":
            insight += " Even though your mood is low, your thoughts show positivity."

        # assessment
        if assessment_level == "high":
            insight += " Your assessment indicates high stress ⚠️."
        elif assessment_level == "moderate":
            insight += " Your assessment shows moderate stress."

        # profile
        if user_concern == "stress":
            insight += " Your patterns suggest stress-related pressure."
        elif user_concern == "anxiety":
            insight += " Your patterns indicate anxiety-related thoughts."
        elif user_concern == "depression":
            insight += " Your patterns indicate low emotional state."

    # ------------------ ACTION ------------------
    if latest_mood == "happy":
        action = "Keep your positive energy! Try journaling what made you feel good today ✨"
    elif latest_mood == "neutral":
        action = "Try a short walk or listen to music 🎧"
    elif latest_mood == "sad":
        action = "Talk to someone you trust or write your thoughts 💬"
    elif latest_mood == "angry":
        action = "Take deep breaths or a short break 🧘"
    else:
        action = "Start tracking your mood regularly."

    # personalize
    if user_concern == "stress":
        action += " Try relaxation techniques like breathing exercises."
    elif user_concern == "anxiety":
        action += " Practice grounding exercises like focusing on your surroundings."
    elif user_concern == "depression":
        action += " Try doing one small enjoyable activity today."

    if user_age == "18-25":
        action += " Managing studies and routine can help reduce pressure."
    elif user_age == "26-40":
        action += " Maintain a healthy work-life balance."
    elif user_age == "41+":
        action += " Prioritize your health and well-being."
    # ------------------ GENERAL TIPS ------------------
    suggestions = [
        "Practice deep breathing",
        "Take short breaks",
        "Stay connected with friends"
    ]

    return render(request, "ai_mood.html", {
        "mood": latest,
        "avg_mood": avg_mood,
        "negative_count": negative_count,
        "risk": risk,
        "insight": insight,
        "trend": trend,
        "suggestions": suggestions,
        "assessment_level": assessment_level,
        "action": action,
        "avg_sentiment": avg_sentiment,
    })
# -------------------- SUPPORT PAGE --------------------
@login_required(login_url='accounts/login')
def support(request):
    return render(request, 'support.html')


# -------------------- PROFILE PAGE --------------------
@login_required
def profile(request):

    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            return redirect("home")

    else:
        form = ProfileForm(instance=profile)

    return render(request, "profile.html", {"form": form})