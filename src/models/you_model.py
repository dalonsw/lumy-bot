import requests
import json

from webscout.AIutel import Optimizers
from webscout.AIutel import Conversation
from webscout.AIutel import AwesomePrompts
from webscout.AIbase import Provider
from webscout import exceptions

class YouChat(Provider):
    def __init__(self, 
                 is_conversation: bool = True, max_tokens: int = 1000, 
                 timeout: int = 10, intro: str = None, filepath: str = None, 
                 update_file: bool = True, proxies: dict = {}, 
                 history_offset: int = 5000, act: str = None,
    ):
        self.session = requests.Session()
        self.is_conversation = is_conversation
        self.max_tokens_to_sample = max_tokens
        self.chat_endpoint = "https://you.com/api/streamingSearch"
        self.stream_chunk_size = 128
        self.timeout = timeout
        self.last_response = {}
        
        # Cache para headers base
        self._base_headers_cache = None
        
        # Políticas persistentes - sempre aplicadas
        self.persistent_policies = intro if intro else ""
        self.policies_enabled = True  # Flag para ativar/desativar políticas

        # Payload otimizado - removeu campos desnecessários
        self.payload = {
            "q": "",
            "domain": "youchat",
            "selectedChatMode": "default",
            "chat": "[]",
        }

        # Headers otimizados
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/event-stream',
            'Connection': 'keep-alive',
        }

        self.__available_optimizers = (
            method
            for method in dir(Optimizers)
            if callable(getattr(Optimizers, method)) and not method.startswith("__")
        )
        self.session.headers.update(self.headers)
        Conversation.intro = (
            AwesomePrompts().get_act(
                act, raise_not_found=True, default=None, case_insensitive=True
            )
            if act
            else intro or Conversation.intro
        )
        self.conversation = Conversation(
            is_conversation, self.max_tokens_to_sample, filepath, update_file
        )
        self.conversation.history_offset = history_offset
        self.session.proxies = proxies

    def ask(
        self,
        prompt: str,
        stream: bool = False,
        raw: bool = False,
        optimizer: str = None,
        conversationally: bool = False,
    ) -> dict:
        # SEMPRE aplica políticas persistentes primeiro
        if self.policies_enabled and self.persistent_policies:
            prompt_with_policies = f"{self.persistent_policies}\n\nUsuário: {prompt}"
        else:
            prompt_with_policies = prompt
        
        # Simplifica processamento - usa prompt direto se conversacional não é necessário
        if self.is_conversation:
            conversation_prompt = self.conversation.gen_complete_prompt(prompt_with_policies)
        else:
            conversation_prompt = prompt_with_policies
            
        # Aplica optimizer apenas se especificado
        if optimizer and optimizer in self.__available_optimizers:
            conversation_prompt = getattr(Optimizers, optimizer)(
                conversation_prompt if conversationally else prompt_with_policies
            )
        
        # Atualiza payload
        self.payload["q"] = conversation_prompt
        
        # Headers otimizados - só atualiza se necessário
        if not self._base_headers_cache:
            self._base_headers_cache = self.headers.copy()
            self.session.headers.update(self._base_headers_cache)

        def for_stream():
            try:
                response = self.session.get(
                    self.chat_endpoint,
                    params=self.payload,
                    stream=True,
                    timeout=self.timeout,
                )

                if not response.ok:
                    raise exceptions.FailedToGenerateResponseError(
                        f"Failed to generate response - ({response.status_code}, {response.reason}) - {response.text[:200]}"
                    )
            except requests.exceptions.Timeout:
                raise exceptions.FailedToGenerateResponseError(
                    f"Request timed out after {self.timeout} seconds"
                )
            except requests.exceptions.RequestException as e:
                raise exceptions.FailedToGenerateResponseError(
                    f"Network error occurred: {str(e)}"
                )

            streaming_response = ""
            response_parts = []  # Lista para otimizar concatenação
            
            # Chunk maior para velocidade
            for line in response.iter_lines(decode_unicode=True, chunk_size=self.stream_chunk_size):
                if line and line.startswith("data:"):
                    json_str = line[5:].strip()  # Remove "data:" mais rápido que regex
                    if json_str:
                        try:
                            data = json.loads(json_str)
                            if "youChatToken" in data:
                                response_parts.append(data["youChatToken"])
                        except json.JSONDecodeError:
                            continue
            
            # Junta todas as partes de uma vez (mais rápido)
            streaming_response = "".join(response_parts)
            # Valida se obtivemos alguma resposta
            if not streaming_response.strip():
                raise exceptions.FailedToGenerateResponseError(
                    "No response received from You.com API"
                )
            
            self.last_response = {"text": streaming_response}  # Mais direto
            
            # Só atualiza histórico se conversacional
            if self.is_conversation:
                self.conversation.update_chat_history(prompt, streaming_response)
                
            return streaming_response

        def for_non_stream():
            for _ in for_stream():
                pass
            return self.last_response

        return for_stream() if stream else for_non_stream()

    def chat(
        self,
        prompt: str,
        stream: bool = False,
        optimizer: str = None,
        conversationally: bool = False,
    ) -> str:
        """Generate response `str`
        Args:
            prompt (str): Prompt to be send.
            stream (bool, optional): Flag for streaming response. Defaults to False.
            optimizer (str, optional): Prompt optimizer name - `[code, shell_command]`. Defaults to None.
            conversationally (bool, optional): Chat conversationally when using optimizer. Defaults to False.
        Returns:
            str: Response generated
        """

        # Simplificado - remove funções aninhadas desnecessárias
        if stream:
            response = self.ask(prompt, True, optimizer=optimizer, conversationally=conversationally)
            return self.get_message(response)
        else:
            response = self.ask(prompt, False, optimizer=optimizer, conversationally=conversationally)
            return self.get_message(response)

    def get_message(self, response) -> str:
        """Extrai a mensagem da resposta de forma otimizada"""
        if isinstance(response, str):
            return response.strip()
        if hasattr(response, 'get'):
            return response.get("text", "").strip()
        return str(response).strip() if response else "Sem resposta disponível"
    
    def set_policies(self, policies: str):
        """Define/atualiza as políticas persistentes"""
        self.persistent_policies = policies
        self.policies_enabled = True
        print("✅ Políticas atualizadas e ativadas")
    
    def enable_policies(self, enable: bool = True):
        """Ativa/desativa as políticas persistentes"""
        self.policies_enabled = enable
        status = "ativadas" if enable else "desativadas"
        print(f"✅ Políticas {status}")
    
    def get_policies(self) -> str:
        """Retorna as políticas atuais"""
        return self.persistent_policies if self.policies_enabled else "Nenhuma política ativa"
    
    def reload_policies_from_file(self, filepath: str):
        """Recarrega políticas de um arquivo"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                policies = f.read()
            self.set_policies(policies)
            print(f"✅ Políticas carregadas de {filepath}")
        except FileNotFoundError:
            print(f"❌ Arquivo não encontrado: {filepath}")
        except Exception as e:
            print(f"❌ Erro ao carregar políticas: {e}")