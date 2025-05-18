from app.schemas.chatbot import ChatbotRequest, ChatbotResponse

class ChatbotService:

    RESPONSE_MAP = {
        ("saldo", "transporte"): "Para consultar seu saldo de transporte, use o endpoint /api/v1/transport/balance.",
        ("documento",): "Você pode gerenciar seus documentos digitais nos endpoints em /api/v1/documents.",
        ("serviço", "prefeitura"): "Esta API simula alguns serviços da prefeitura. Quais serviços específicos você procura?",
        ("olá", "oi", "ajuda"): "Olá! Como posso ajudar com sua carteira digital municipal?",
    }
    DEFAULT_RESPONSE = "Desculpe, não entendi sua pergunta. Posso ajudar com informações sobre saldo de transporte ou documentos digitais?"

    def get_chatbot_response(self, question: str) -> str:
        """
        Returns a predefined response based on the user's question using a dictionary for mapping keywords to responses.
        """
        question_lower = question.lower()

        for keywords, response in self.RESPONSE_MAP.items():
            if any(keyword in question_lower for keyword in keywords):
                return response
        return self.DEFAULT_RESPONSE