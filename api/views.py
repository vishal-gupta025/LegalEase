from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rag.simple_rag_llm import ask_question
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from cases.models import LegalCase
from documents.models import LegalDocument
from documents.services.document_processor import LegalDocumentProcessor

USER_CHAT_HISTORY = {}


class RegisterApi(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serialzer = RegisterSerializer(data=request.data)
        if serialzer.is_valid():
            serialzer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        
class LoginApi(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = User.objects.filter(username=username).first()
        if user is None:
            return Response({"error": "Username not found"}, status=status.HTTP_404_NOT_FOUND)
        if not user.check_password(password):
            return Response({"error": "Incorrect password"}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })

class AskQuestionApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        question = (request.data.get("question") or "").strip()

        if not question:
            return Response({"error": "Question is required."}, status=status.HTTP_400_BAD_REQUEST)
        

        history = USER_CHAT_HISTORY.get(user.username, [])

        history_text = ""
        for h in history:
            history_text += f"User: {h['user']}\nAssistant: {h['assistant']}\n"

        # send to RAG + LLM
        answer = ask_question(
            question=question,
            chat_history=history_text
        )

        # save back to history
        history.append({
            "user": question,
            "assistant": answer
        })
        USER_CHAT_HISTORY[user.username] = history

        return Response({
            "user": user.username,
            "question": question,
            "answer": answer
        })

class UploadDocumentAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        title = request.data.get("title")
        case_number = request.data.get("case_number")
        court = request.data.get("court")
        parties = request.data.get("parties")
        file = request.FILES.get("file")

        if not all([title, case_number, court, parties, file]):
            return Response(
                {"error": "title, case_number, court, parties and file are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 1. Create LegalCase
        legal_case = LegalCase.objects.create(
            title=title,
            case_number=case_number,
            court=court,
            parties_involved=parties,
            date_of_judgment="2024-01-01"  # temporary, you can make this dynamic later
        )

        # 2. Create LegalDocument
        legal_document = LegalDocument.objects.create(
            legal_case=legal_case,
            file=file,
            original_filename=file.name
        )

        # 3. Process document (extract + sections)
        LegalDocumentProcessor.process_document(legal_document)

        return Response({
            "message": "Document uploaded and processed successfully",
            "case_id": legal_case.id,
            "document_id": legal_document.id
        }, status=status.HTTP_201_CREATED)
