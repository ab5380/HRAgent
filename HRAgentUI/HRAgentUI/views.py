# from django.http import HttpResponse

# def homepage(request):
#   return HttpResponse("Hello World! This is teh home page")

# def about(request):
#   return HttpResponse("My About Page")


from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import default_storage
import os
import smtplib
import ssl
from email.message import EmailMessage
from textwrap import dedent
from dotenv import load_dotenv
from crewai import Crew, Agent, Task, Process
from datetime import datetime, timedelta
from crewai_tools import DOCXSearchTool, CSVSearchTool, TXTSearchTool, tool, SerperDevTool
from dotenv import load_dotenv

load_dotenv()

doc_search = DOCXSearchTool("/Users/aneeshbukya/Desktop/Projects/HRAgent/HRAgentUI/HRAgentUI/Employee-Code-of-Conduct.docx")
google_search = SerperDevTool()

def homepage(request):
  return render(request,'home.html')

def about(request):
  return render(request,'about.html')

def candidate_notes(request):
  return render(request,"notes.html")

def faq_agent(request):
  return render(request,"faq.html")

def onboarding(request):
  return render(request,"email.html")


@csrf_exempt
def summarize_notes(request):
    if request.method == 'POST':
        candidate_name = request.POST['candidateName']
        notes_file = request.FILES['notesFile']
        file_path = default_storage.save('tmp/' + notes_file.name, notes_file)

        txt_search = TXTSearchTool(file_path)

        notes_agent = Agent(
            role="Candidate Notes Summarizer",
            goal='Summarizes the notes on a candidate',
            backstory=dedent("""\
                As a Notes Summarizer, your mission is to read through the entire file
                and summarize the information in a concise yet informative manner into bullet points."""),
            tools=[txt_search],
            verbose=True
        )

        def candidate_notes_task(name):
            return Task(
                description=dedent(f"""\
                    Summarize the document into a few detailed bullet points
                    Candidate Name: {name}"""),
                expected_output=dedent("""\
                    Ensure each bullet point isn't longer than 80 characters
                    Have a list of 5-6 bullet points on notes given about the candidate
                    Use this format for your output:
                    Candidate Name : [Candidate Name]
                    - Candidate notes"""),
                agent=notes_agent,
            )

        candidate_task = candidate_notes_task(candidate_name)

        crew = Crew(agents=[notes_agent], tasks=[candidate_task])
        result = crew.kickoff()
        print(result)

        # Clean up the temporary file
        os.remove(file_path)

        return JsonResponse({'summary': result})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def process_form(request):
    if request.method == 'POST':
        question = request.POST.get('question')

        if not question:
            return JsonResponse({'summary': 'Please provide a question.'}, status=400)

        try:
            # Create an instance of DOCXSearchTool with the document

            faq_agent = Agent(
                role='Human Resource Employee',
                goal='Find the section of the document which contains relevant information and summarize them.',
                tools=[doc_search],
                backstory=dedent("""\
                    As a HR Employee, your mission is to find which sections of the document contains the
                    relevant information and summarize those in a few sentences. If you can't find any keywords then just say 
                    I couldn't find anything in our company's policy regarding this topic. Kindly 
                    contact HR for information on this topic."""),
                verbose=True
            )

            def summary_task(question):
                return Task(
                    description=dedent(f"""\
                        Find all the relevant areas of the document where the words from the question appear and
                        summarize them in a few words.
                        Question: {question}"""),
                    expected_output=dedent("""\
                        Give a single conclusive answer using the relevant information in the document which 
                        contains the keyword asked in the question. Answer the question with a yes or no.
                     Start each answer with yes or no and then say' our company policy states that'. Answer should not be longer than 2-3 sentences."""),
                    agent=faq_agent
                )

            summarize_task = summary_task(question)

            crew = Crew(agents=[faq_agent], tasks=[summarize_task])
            result = crew.kickoff()

            return JsonResponse({'summary': result})

        except Exception as e:
            return JsonResponse({'summary': f'An error occurred: {str(e)}'}, status=500)

    return JsonResponse({'summary': 'Invalid request method.'}, status=405)

# @csrf_exempt
# def onboarding_submit(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         role = request.POST.get('role')
#         email = request.POST.get('email')
#         code_of_conduct = request.POST.get('codeOfConduct')

#         # Define your agents, tasks, and crew as per your requirements
#         researcher_agent = Agent(
#             role="Research Specialist",
#             goal='Research the role to find the best practices for the job role and provide links on how to be successful ',
#             tools=[google_search],
#             backstory=dedent("""\
#               As a Research Specialist, your job is to search the web and come up with the best practices and methods
#               to be successful at a specific job role and also provide useful links which talk about how to be successful
#               in the particular job role."""),
#             verbose=True
#         )

#         def research_task(role):
#             return Task(
#                 description=dedent(f"""\
#                     generate the best practices and ways a person can successful at the given job role
#                     Job Role: {role}"""),
#                 expected_output=dedent("""\
#                     The best practices and things to do to be successful at the job role along with useful links for reference"""),
#                 agent=researcher_agent,
#             )

#         set_research_task = research_task(role)

#         greet_agent = Agent(
#             role="Personalized Message Sender",
#             goal='Write a personalized message to person and welcome them into the company ',
#             backstory=dedent("""\
#               Your job is to write a personalized message to the new employee joining the company and talk about company culture and wish
#               the employee success in the company"""),
#             verbose=True
#         )

#         def onboard_task(name, link):
#             return Task(
#                 description=dedent(f"""\
#                     onboard the people by wishing good luck and ask them to review the code of conduct
#                     Employee Code of Conduct Link: {link},
#                     Name: {name}"""),
#                 expected_output=dedent("""\
#                     Output should be formatted like this:
#                     - Greeting and well wishes 
#                     - Ask to review Employee Code of Conduct with link 
#                     - Best Practices to be successful along with links
#                     - end it with
#                     Best Regards,
#                     John McEnroe,
#                     HR of Company XYZ"""),
#                 agent=greet_agent,
#                 context=[set_research_task]
#             )

#         set_onboard_task = onboard_task(name, link=code_of_conduct)

#         crew = Crew(agents=[researcher_agent, greet_agent], tasks=[set_research_task, set_onboard_task])
#         # Get your crew to work!
#         result = crew.kickoff()

#         # Define email sender and receiver
#         email_sender = os.getenv('EMAIL_SENDER')
#         email_password = os.getenv('EMAIL_PASSWORD')
#         email_receiver = email
        
#         # Check if the environment variables are loaded correctly
#         if not email_sender or not email_password:
#             raise ValueError("Email credentials are not set in the environment variables")
        
#         # Set the subject and body of the email
#         subject = 'Welcome to Company XYZ!!!'
#         body = result

#         em = EmailMessage()
#         em['From'] = email_sender
#         em['To'] = email_receiver
#         em['Subject'] = subject
#         em.set_content(body)

#         # Add SSL (layer of security)
#         context = ssl.create_default_context()

#         # Log in and send the email
#         with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
#             smtp.login(email_sender, email_password)
#             smtp.sendmail(email_sender, email_receiver, em.as_string())

#         # Returning a JSON response indicating success
#         return JsonResponse({'message': 'Email sent successfully!', 'result': result})
#     else:
#         return JsonResponse({'message': 'Invalid request method!'}, status=400)


def onboarding_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        role = request.POST.get('role')
        email = request.POST.get('email')
        code_of_conduct = request.POST.get('codeOfConduct')

        # # Define your agents, tasks, and crew as per your requirements
        # researcher_agent = Agent(
        #     role="Research Specialist",
        #     goal='Research the role to find the best practices for the job role and provide links on how to be successful ',
        #     tools=[google_search],
        #     backstory=dedent("""\
        #       As a Research Specialist, your job is to search the web and come up with the best practices and methods
        #       to be successful at a specific job role and also provide useful links which talk about how to be successful
        #       in the particular job role."""),
        #     verbose=True
        # )

        # def research_task(role):
        #     return Task(
        #         description=dedent(f"""\
        #             generate the best practices and ways a person can successful at the given job role
        #             Job Role: {role}"""),
        #         expected_output=dedent("""\
        #             The best practices and things to do to be successful at the job role along with useful links for reference"""),
        #         agent=researcher_agent,
        #     )

        # set_research_task = research_task(role)

        greet_agent = Agent(
            role="Personalized Message Sender and Research Specialist",
            goal='Write a personalized message to person and welcome them into the company. Also, Research the role to find the best practices for the job role and provide links on how to be successful.',
            backstory=dedent("""\
              Your job is to write a personalized message to the new employee joining the company and talk about company culture and wish
              the employee success in the company.Also, your job is to search the web and come up with the best practices and methods
              to be successful at a specific job role and also provide useful links which talk about how to be successful
              in the particular job role. """),
            verbose=True
        )

        def onboard_task(name, link):
            return Task(
                description=dedent(f"""\
                    onboard the people by wishing good luck and ask them to review the code of conduct.generate the best practices and ways a person can successful at the given job role
                    Employee Code of Conduct Link: {link},
                    Job Role: {role},
                    Name: {name}"""),
                expected_output=dedent("""\
                    Output should be formatted like this:
                    - Greeting and well wishes 
                    - Ask to review Employee Code of Conduct with link 
                    - Best Practices to be successful along with links
                    - end it with
                    Best Regards,
                    John McEnroe,
                    HR of Company XYZ"""),
                agent=greet_agent,
            )

        set_onboard_task = onboard_task(name, link=code_of_conduct)

        crew = Crew(agents=[greet_agent], tasks=[set_onboard_task])
        # Get your crew to work!
        result = crew.kickoff()

        # Define email sender and receiver
        email_sender = os.getenv('EMAIL_SENDER')
        email_password = os.getenv('EMAIL_PASSWORD')
        email_receiver = email
        
        # Check if the environment variables are loaded correctly
        if not email_sender or not email_password:
            raise ValueError("Email credentials are not set in the environment variables")
        
        # Set the subject and body of the email
        subject = 'Welcome to Company XYZ!!!'
        body = result

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        # Add SSL (layer of security)
        context = ssl.create_default_context()

        # Log in and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

        # Returning a JSON response indicating success
        return JsonResponse({'message': 'Email sent successfully!', 'result': result})
    else:
        return JsonResponse({'message': 'Invalid request method!'}, status=400)
