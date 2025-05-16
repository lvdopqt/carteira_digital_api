from app.schemas.chatbot import ChatbotRequest, ChatbotResponse # Importe os schemas

class ChatbotService:
    def get_chatbot_response(self, question: str) -> str:
        """
        Retorna uma resposta pré-definida baseada na pergunta do usuário (lógica mockada).
        """
        question_lower = question.lower()

        if "saldo" in question_lower or "transporte" in question_lower:
            return "Para consultar seu saldo de transporte, use o endpoint /api/v1/transport/balance."
        elif "documento" in question_lower:
            return "Você pode gerenciar seus documentos digitais nos endpoints em /api/v1/documents."
        elif "serviço" in question_lower or "prefeitura" in question_lower:
             return "Esta API simula alguns serviços da prefeitura. Quais serviços específicos você procura?"
        elif "olá" in question_lower or "oi" in question_lower or "ajuda" in question_lower:
             return "Olá! Como posso ajudar com sua carteira digital municipal?"
        else:
            return "Desculpe, não entendi sua pergunta. Posso ajudar com informações sobre saldo de transporte ou documentos digitais?"