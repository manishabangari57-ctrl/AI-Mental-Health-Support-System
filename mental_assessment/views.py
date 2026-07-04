from django.shortcuts import render
from .forms import AssessmentForm
from .models import Assessment
from django.contrib.auth.decorators import login_required

@login_required(login_url="/accounts/login/")
def assessment_view(request):

    if request.method == "POST":

        form = AssessmentForm(request.POST)

        if form.is_valid():

            q1 = int(form.cleaned_data["q1"])
            q2 = int(form.cleaned_data["q2"])
            q3 = int(form.cleaned_data["q3"])
            q4 = int(form.cleaned_data["q4"])
            q5 = int(form.cleaned_data["q5"])

            score = q1 + q2 + q3 + q4 + q5

            if score <= 5:
                result = "low"
                message = "Your stress level appears low. Keep maintaining healthy habits."

            elif score <= 10:
                result = "moderate"
                message = "You may be experiencing moderate stress. Try relaxation exercises."

            else:
                result = "high"
                message = "Your stress level appears high. Consider talking to someone or seeking support."

            Assessment.objects.create( 
                user=request.user,
                q1=q1,
                q2=q2,
                q3=q3,
                q4=q4,
                q5=q5,
                score=score,
                level=result
            )

            return render(request,"assessment_result.html",{
                "result":result,
                "message":message
            })

    else:
        form = AssessmentForm()

    return render(request,"assessment.html",{"form":form})


def assessment_history(request):

    assessments = Assessment.objects.all().order_by('-date')

    return render(request,"assessment_history.html",{
        "assessments":assessments
    })