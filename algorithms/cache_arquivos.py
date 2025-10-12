class CacheArquivos:

    def __init__(self):
        self.ordem: list[int] = []   # lista de dicionarios com nome e conteudo

        self.cache: dict[int, str] = {}

        self.max_size: int = 10

        self.hits: int = 0

        self.requests: int = 0



    def get_hits(self) -> int:

        return self.hits



    def inc_hits(self):

        self.hits += 1



    def get_requests(self) -> int:

        return self.requests



    def inc_requests(self):

        self.requests += 1



    def get_max_size(self) -> int:

        return self.max_size



    def get_arquivo_pelo_id(self, id_arquivo: int) -> str:

        """

        Retorna o conteúdo do arquivo (str).

        """

        return self.cache[id_arquivo]



    def contem_arquivo(self, id_arquivo: int) -> bool:

        return id_arquivo in self.cache



    def add_arquivo(self, id_arquivo: int, conteudo: str) -> bool:

        """

        Adiciona arquivo (no formato {'nome':id_arquivo, 'conteudo':conteudo}) no final da lista cache se não estiver cheio.

        Retorna True caso a inserção ocorra com sucesso e False caso contrario



        Args:

            id_arquivo (int): número identificador do arquivo

            conteudo (str): conteúdo do arquivo



        Returns:

            bool: Sucesso da operação

        """

        if id_arquivo in self.cache:

            # atualiza conteúdo (não altera ordem)

            self.cache[id_arquivo] = conteudo

            return True



        if len(self.ordem) >= self.max_size:

            # cheio: sinaliza falha

            return False



        # cabe: insere no final (mais novo)

        self.ordem.append(id_arquivo)

        self.cache[id_arquivo] = conteudo

        return True



    def remover_ultimo(self) -> dict:

        """Remove o último inserido (mais novo). Retorna dict {'nome': id, 'conteudo': conteudo}"""

        id_removido = self.ordem.pop()  # último

        conteudo = self.cache.pop(id_removido)

        return {"nome": id_removido, "conteudo": conteudo}



    def remover_primeiro(self) -> dict:

        """Remove o primeiro inserido (mais antigo)."""

        id_removido = self.ordem.pop(0)

        conteudo = self.cache.pop(id_removido)

        return {"nome": id_removido, "conteudo": conteudo}



    def remover(self, idx: int) -> dict:

        """

        Remove por índice na ordem atual. Retorna dict como acima.

        (Mantive esse método conforme seu original.)

        """

        id_removido = self.ordem.pop(idx)

        conteudo = self.cache.pop(id_removido)

        return {"nome": id_removido, "conteudo": conteudo}



    def move_para_final(self, id_arquivo: int) -> None:

        """

        Move o id para o final da ordem (marca como o mais recentemente usado).

        Operação O(n) por usar list.remove, mas simples e adequada para caches pequenos.

        """

        if id_arquivo in self.cache:

            self.ordem.remove(id_arquivo)

            self.ordem.append(id_arquivo)


