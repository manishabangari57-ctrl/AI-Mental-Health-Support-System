from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MoodForm
from .models import Mood
import json
from collections import defaultdict
from textblob import TextBlob
from django.utils import timezone
from datetime import timedelta

# ------------------ MOOD TRACKER ------------------
@login_required(login_url="/accounts/login/")
def mood_tracker(request):
    from_ai = request.GET.get("from_ai")

    # ✅ always define form
    form = MoodForm()

    if request.method == "POST":
        form = MoodForm(request.POST)

        if form.is_valid():
            mood_obj = form.save(commit=False)
            note = mood_obj.note if mood_obj.note else ""

            if note:
              polarity = TextBlob(note).sentiment.polarity

              if polarity > 0.2:
                mood_obj.sentiment = "positive"
              elif polarity < -0.2:
                mood_obj.sentiment = "negative"
              else:
                mood_obj.sentiment = "neutral"
            else:
              mood_obj.sentiment = "neutral"
            # 🔥 attach user
            mood_obj.user = request.user

            mood_obj.save()

            # 🔥 redirect flow
            if from_ai == "true":
                return redirect("ai_mood")

            return redirect("mood")

        else:
            print("FORM ERROR:", form.errors)

    # ✅ last 7 days data
    last_week = timezone.now() - timedelta(days=7)

    moods = Mood.objects.filter(
        user=request.user,
        date__gte=last_week
    ).order_by("date")

    # ✅ mood mapping
    mood_map = {
        "angry": 1,
        "sad": 2,
        "neutral": 3,
        "happy": 4
    }

    # ✅ chart data
    dates = []
    mood_values = []
    

    for m in moods:
        dates.append(m.date.strftime("%b %d"))   # clean labels
        mood_values.append(mood_map.get(m.mood.lower(), 3))
    

    return render(request, "mood.html", {
        "form": form,
        "moods": moods,
        "dates": json.dumps(dates),
        "mood_values": json.dumps(mood_values),
        "from_ai": from_ai,
    })

# ------------------ MOOD HISTORY ------------------
