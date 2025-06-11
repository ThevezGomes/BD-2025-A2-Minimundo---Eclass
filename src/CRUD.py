import psycopg2
from psycopg2 import sql
import sys
from datetime import datetime

class EClassCRUD:
    """
    Uma classe para gerenciar o banco de dados da plataforma de e-learning eClass via CLI.
    Lida com operações para usuários, cursos, matrículas, conteúdo, grupos, mensagens e relatórios.
    """
    def __init__(self):
        self.conn = None
        self.cur = None
        self.connect()

    def connect(self):
        """Estabelece a conexão com o banco de dados PostgreSQL."""
        try:
            # IMPORTANTE: Altere 'dbname' se o nome do seu banco de dados for diferente.
            self.conn = psycopg2.connect(dbname="josethevez")
            self.cur = self.conn.cursor()
            self.cur.execute("SET search_path TO eclass;")
            self.conn.commit()
            print("✅ Conexão com o PostgreSQL estabelecida com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao conectar ao PostgreSQL: {e}")
            sys.exit(1)

    def disconnect(self):
        """Fecha a conexão com o banco de dados."""
        if self.cur: self.cur.close()
        if self.conn: self.conn.close()
        print("\n🔌 Conexão com o PostgreSQL encerrada.")

    # --- Métodos Auxiliares ---
    def _get_user_info(self, user_id):
        try:
            user_id = int(user_id)
            self.cur.execute("SELECT primnomeuser, sobrenomeuser, (SELECT matriculaaluno FROM aluno WHERE iduser = u.iduser) FROM usuario u WHERE u.iduser = %s", (user_id,))
            user = self.cur.fetchone()
            if user:
                return (f"{user[0]} {user[1]}", user[2] or "N/A (Não é Aluno)")
            return ("Usuário Desconhecido", "N/A")
        except (ValueError, TypeError):
            return ("Usuário Desconhecido", "N/A")
            
    def _get_user_roles(self, user_id):
        roles = []
        try:
            user_id = int(user_id)
            self.cur.execute("SELECT 1 FROM aluno WHERE iduser = %s", (user_id,))
            if self.cur.fetchone(): roles.append("Aluno")
            self.cur.execute("SELECT 1 FROM professor WHERE iduser = %s", (user_id,))
            if self.cur.fetchone(): roles.append("Professor")
            self.cur.execute("SELECT 1 FROM monitor WHERE iduser = %s", (user_id,))
            if self.cur.fetchone(): roles.append("Monitor")
            return roles
        except(ValueError, TypeError):
            return []

    def _get_discipline_name(self, codigo_disc):
        if not codigo_disc: return "Disciplina Desconhecida"
        self.cur.execute("SELECT nomedisc FROM disciplina WHERE codigodisc = %s", (codigo_disc,))
        disc = self.cur.fetchone()
        return disc[0] if disc else "Disciplina Desconhecida"
    
    def _get_activity_info(self, id_ativ):
        try:
            id_ativ = int(id_ativ)
            self.cur.execute("SELECT nomeativ, tipoativ FROM atividade WHERE idativ = %s", (id_ativ,))
            activity = self.cur.fetchone()
            return (activity[0], activity[1]) if activity else ("Atividade Desconhecida", "N/A")
        except (ValueError, TypeError):
            return ("Atividade Desconhecida", "N/A")

    def _get_next_id(self, table, id_column):
        query = sql.SQL("SELECT COALESCE(MAX({}), 0) + 1 FROM {}").format(sql.Identifier(id_column), sql.Identifier(table))
        self.cur.execute(query)
        return self.cur.fetchone()[0]
    
    def _press_enter_to_continue(self):
        input("\nPressione Enter para continuar...")

    def analisar_e_executar_consulta(self, query, params=None):
        """
        Executa uma consulta com EXPLAIN ANALYZE, imprime um resumo do tempo
        e, depois, executa a consulta normal e imprime os resultados.
        """
        if not query.strip().upper().startswith("SELECT"):
            print("❌ ERRO: Apenas consultas SELECT podem ser analisadas com esta função.")
            return

        # Etapa 1: EXPLAIN ANALYZE para obter o plano e os tempos
        explain_query = "EXPLAIN (ANALYZE, VERBOSE) " + query
        print("\n" + "="*70)
        print(f"🔎 Analisando Performance da Consulta...")
        print("="*70)

        tempo_sem_indice = None
        tempo_com_indice = None

        # Verifica se tem indices
        try:
            self.cur.execute("DROP INDEX IF EXISTS aluno_index;")
            self.cur.execute("DROP INDEX IF EXISTS prof_index;")
            self.cur.execute("DROP INDEX IF EXISTS monit_index;")
            self.cur.execute("DROP INDEX IF EXISTS user_index;")

        except Exception as e:
            print(f"❌ Ocorreu um erro ao remover o índice: {e}")
            self.conn.rollback()
            return
        
        try:
            self.cur.execute(explain_query, params)
            plan = self.cur.fetchall()
            
            print("--- RESUMO DA ANÁLISE DE PERFORMANCE (SEM ÍNDICE) ---")
            for row in plan:
                if "Planning Time:" in row[0] or "Execution Time:" in row[0]:
                    print(row[0].strip())
                if "Execution Time:" in row[0]:
                    tempo_sem_indice = float(row[0].strip().split()[2])
            print("-" * 70)

        except Exception as e:
            print(f"❌ Ocorreu um erro ao analisar a consulta: {e}")
            self.conn.rollback()
            return
        
        # Colocar index
        try:
            self.cur.execute("CREATE INDEX aluno_index ON alunodisc(iduser);")
            self.cur.execute("CREATE INDEX prof_index ON profdisc(iduser);")
            self.cur.execute("CREATE INDEX monit_index ON monitdisc(iduser);")
            self.cur.execute("CREATE INDEX user_index ON usuario(primnomeuser);")
            
            print("Índices Criados")
            print("-" * 70)

        except Exception as e:
            print(f"❌ Ocorreu um erro ao criar o índice: {e}")
            self.conn.rollback()
            return
        
        try:
            self.cur.execute(explain_query, params)
            plan = self.cur.fetchall()
            
            print("--- RESUMO DA ANÁLISE DE PERFORMANCE (COM ÍNDICE) ---")
            for row in plan:
                if "Planning Time:" in row[0] or "Execution Time:" in row[0]:
                    print(row[0].strip())
                if "Execution Time:" in row[0]:
                    tempo_com_indice = float(row[0].strip().split()[2])
            print(f"Melhora do tempo de execução em: {tempo_sem_indice / tempo_com_indice} vezes")
            print("-" * 70)

        except Exception as e:
            print(f"❌ Ocorreu um erro ao analisar a consulta: {e}")
            self.conn.rollback()
            return

        # Etapa 2: Executar a consulta SELECT normal e mostrar os dados
        print("\n--- RESULTADOS DA CONSULTA (SELECT) ---")
        try:
            self.cur.execute(query, params)
            results = self.cur.fetchall()
            
            if not results:
                print("A consulta não retornou resultados.")
            else:
                colnames = [desc[0] for desc in self.cur.description]
                print(" | ".join(f"{col:<30}" for col in colnames))
                print("-" * (33 * len(colnames)))
                for row in results:
                    print(" | ".join(f"{str(item):<30}" for item in row))
            print("="*70)

        except Exception as e:
            print(f"❌ Ocorreu um erro ao executar a consulta SELECT: {e}")
            self.conn.rollback()

        # Remover index
        try:
            self.cur.execute("DROP INDEX aluno_index;")
            self.cur.execute("DROP INDEX prof_index;")
            self.cur.execute("DROP INDEX monit_index;")
            self.cur.execute("DROP INDEX user_index;")
            
            print("Índices Removidos")
            print("-" * 70)

        except Exception as e:
            print(f"❌ Ocorreu um erro ao remover o índice: {e}")
            self.conn.rollback()
            return


    # --- 1. Gerenciamento de Usuários ---
    def submenu_usuarios(self):
        while True:
            print("\n--- 👤 Gerenciamento de Usuários ---")
            print("1. Criar Novo Usuário")
            print("2. Gerenciar Papéis de um Usuário (Adicionar/Remover)")
            print("3. Listar Usuários")
            print("4. Atualizar Dados de um Usuário")
            print("5. Deletar Usuário")
            print("6. Voltar ao Menu Principal")
            
            escolha = input("Escolha uma opção: ")
            if escolha == '1': self.criar_usuario()
            elif escolha == '2': self.gerenciar_papeis_usuario()
            elif escolha == '3': self.listar_usuarios(prompt=True)
            elif escolha == '4': self.atualizar_usuario()
            elif escolha == '5': self.deletar_usuario()
            elif escolha == '6': break
            else: print("❌ Opção inválida.")
            if escolha in ['1', '2', '3', '4', '5']: self._press_enter_to_continue()

    def criar_usuario(self):
        print("\n--- Criar Novo Usuário ---")
        prim_nome = input("Primeiro Nome: ")
        sobrenome = input("Sobrenome: ")
        if not prim_nome or not sobrenome:
            print("❌ Nome e sobrenome são obrigatórios.")
            return

        user_id = self._get_next_id('usuario', 'iduser')
        query = "INSERT INTO usuario (iduser, primnomeuser, sobrenomeuser) VALUES (%s, %s, %s)"
        self.cur.execute(query, (user_id, prim_nome, sobrenome))
        self.conn.commit()
        print(f"\n✅ SUCESSO: Usuário '{prim_nome} {sobrenome}' (ID: {user_id}) foi criado.")

    def gerenciar_papeis_usuario(self):
        print("\n--- Gerenciar Papéis de um Usuário ---")
        self.listar_usuarios(prompt=False)
        try:
            user_id_str = input("\nDigite o ID do usuário para gerenciar os papéis: ")
            user_id = int(user_id_str)
            nome_usuario, _ = self._get_user_info(user_id)
            if nome_usuario == "Usuário Desconhecido":
                print("❌ ID de usuário não encontrado.")
                return
        except (ValueError, TypeError):
            print("❌ ID inválido.")
            return
            
        while True:
            papeis_atuais = self._get_user_roles(user_id)
            print(f"\nGerenciando papéis para: {nome_usuario} (ID: {user_id})")
            print(f"Papéis Atuais: {', '.join(papeis_atuais) or 'Nenhum'}")
            print("\n1. Adicionar Papel")
            print("2. Remover Papel")
            print("3. Concluir e Voltar")
            
            escolha = input("Escolha uma opção: ")
            if escolha == '1':
                self._adicionar_papel(user_id, papeis_atuais)
            elif escolha == '2':
                self._remover_papel(user_id, papeis_atuais)
            elif escolha == '3':
                break
            else:
                print("❌ Opção inválida.")
    
    def _adicionar_papel(self, user_id, papeis_atuais):
        todos_papeis = {"Aluno", "Professor", "Monitor"}
        papeis_disponiveis = sorted(list(todos_papeis - set(papeis_atuais)))
        if not papeis_disponiveis:
            print("ℹ️ Este usuário já possui todos os papéis disponíveis.")
            return
            
        print("\nSelecione um papel para ADICIONAR:")
        for i, papel in enumerate(papeis_disponiveis, 1):
            print(f"{i}. {papel}")
        
        try:
            escolha = int(input("Escolha uma opção: "))
            if 1 <= escolha <= len(papeis_disponiveis):
                papel_para_adicionar = papeis_disponiveis[escolha-1].lower()
                
                if papel_para_adicionar == 'aluno':
                    matricula = int(input("Digite a matrícula do aluno: "))
                    self.cur.execute("INSERT INTO aluno (iduser, matriculaaluno) VALUES (%s, %s)", (user_id, matricula))
                else:
                    query = sql.SQL("INSERT INTO {} (iduser) VALUES (%s)").format(sql.Identifier(papel_para_adicionar))
                    self.cur.execute(query, (user_id,))
                
                self.conn.commit()
                print(f"✅ SUCESSO: Papel de '{papel_para_adicionar.capitalize()}' adicionado.")
            else:
                print("❌ Opção inválida.")
        except psycopg2.errors.UniqueViolation:
            self.conn.rollback()
            print("❌ ERRO: Matrícula já existe.")
        except (ValueError, TypeError):
            self.conn.rollback()
            print("❌ ERRO: Entrada inválida. Matrícula deve ser um número.")
        except Exception as e:
            self.conn.rollback()
            print(f"❌ ERRO Inesperado: {e}")

    def _remover_papel(self, user_id, papeis_atuais):
        if not papeis_atuais:
            print("ℹ️ Este usuário não possui papéis para remover.")
            return

        print("\nSelecione um papel para REMOVER:")
        for i, papel in enumerate(papeis_atuais, 1):
            print(f"{i}. {papel}")
            
        try:
            escolha = int(input("Escolha uma opção: "))
            if 1 <= escolha <= len(papeis_atuais):
                papel_para_remover = papeis_atuais[escolha-1].lower()
                
                tabela_vinculo = {'aluno': 'alunodisc', 'professor': 'profdisc', 'monitor': 'monitdisc'}
                self.cur.execute(sql.SQL("SELECT 1 FROM {} WHERE iduser = %s").format(sql.Identifier(tabela_vinculo[papel_para_remover])), (user_id,))
                if self.cur.fetchone():
                    print(f"❌ ERRO: Não é possível remover o papel de '{papel_para_remover.capitalize()}' pois o usuário está vinculado a disciplinas com esse papel.")
                    return

                query = sql.SQL("DELETE FROM {} WHERE iduser = %s").format(sql.Identifier(papel_para_remover))
                self.cur.execute(query, (user_id,))
                self.conn.commit()
                print(f"✅ SUCESSO: Papel de '{papel_para_remover.capitalize()}' removido.")
            else:
                print("❌ Opção inválida.")
        except psycopg2.IntegrityError:
            self.conn.rollback()
            print(f"❌ ERRO: Não é possível remover o papel. Existem outros vínculos no sistema (entregas, grupos, etc.).")
        except (ValueError, TypeError):
            print("❌ ERRO: Escolha inválida.")
        except Exception as e:
            self.conn.rollback()
            print(f"❌ ERRO Inesperado: {e}")
            
    def listar_usuarios(self, prompt=False):
        tipo_choice = '1'
        if prompt:
            print("\n--- Listar Usuários ---")
            print("1. Todos")
            print("2. Apenas Alunos")
            print("3. Apenas Professores")
            print("4. Apenas Monitores")
            tipo_choice = input("Escolha o tipo de usuário a listar: ") or '1'
        
        base_query = "SELECT u.iduser, u.primnomeuser, u.sobrenomeuser FROM usuario u"
        if tipo_choice == '2':
            query = "SELECT u.iduser, u.primnomeuser, u.sobrenomeuser, a.matriculaaluno FROM usuario u JOIN aluno a ON u.iduser = a.iduser ORDER BY u.primnomeuser"
            title = "Alunos"
        elif tipo_choice == '3':
            query = "SELECT u.iduser, u.primnomeuser, u.sobrenomeuser FROM usuario u JOIN professor p ON u.iduser = p.iduser ORDER BY u.primnomeuser"
            title = "Professores"
        elif tipo_choice == '4':
            query = "SELECT u.iduser, u.primnomeuser, u.sobrenomeuser FROM usuario u JOIN monitor m ON u.iduser = m.iduser ORDER BY u.primnomeuser"
            title = "Monitores"
        else:
            query = base_query + " ORDER BY u.primnomeuser"
            title = "Todos os Usuários"

        self.cur.execute(query)
        usuarios = self.cur.fetchall()
        
        print(f"\n--- 📋 Lista de {title} ---")
        if not usuarios:
            print("Nenhum usuário encontrado.")
            return []
        
        for user in usuarios:
            roles = self._get_user_roles(user[0])
            matricula_info = f", Matrícula: {user[3]}" if tipo_choice == '2' else ""
            print(f"ID: {user[0]}, Nome: {user[1]} {user[2]}{matricula_info} | Papéis: {', '.join(roles) or 'Nenhum'}")
        return usuarios

    def atualizar_usuario(self):
        self.listar_usuarios(prompt=False)
        user_id_str = input("\nDigite o ID do usuário para atualizar os dados: ")
        nome_antigo, _ = self._get_user_info(user_id_str)
        if nome_antigo == "Usuário Desconhecido":
            print("❌ ID de usuário não encontrado.")
            return
        
        print("\nDeixe em branco para não alterar.")
        prim_nome = input(f"Novo Primeiro Nome: ") or None
        sobrenome = input(f"Novo Sobrenome: ") or None
        
        updates, params = [], []
        if prim_nome:
            updates.append("primnomeuser = %s")
            params.append(prim_nome)
        if sobrenome:
            updates.append("sobrenomeuser = %s")
            params.append(sobrenome)
        
        if not updates:
            print("Nenhuma alteração fornecida.")
            return

        query = sql.SQL("UPDATE usuario SET {} WHERE iduser = %s").format(sql.SQL(', ').join(map(sql.SQL, updates)))
        params.append(user_id_str)
        self.cur.execute(query, tuple(params))
        self.conn.commit()
        novo_nome, _ = self._get_user_info(user_id_str)
        print(f"\n✅ SUCESSO: Usuário '{nome_antigo}' (ID: {user_id_str}) atualizado para '{novo_nome}'.")

    def deletar_usuario(self):
        self.listar_usuarios(prompt=False)
        user_id_str = input("\nDigite o ID do usuário a ser deletado: ")
        nome, _ = self._get_user_info(user_id_str)
        if nome == "Usuário Desconhecido":
            print("❌ ID de usuário não encontrado.")
            return
        
        confirm = input(f"Tem certeza que deseja deletar o usuário '{nome}' (ID: {user_id_str})? Esta ação é irreversível. (s/n): ").lower()
        if confirm == 's':
            try:
                self.cur.execute("DELETE FROM usuario WHERE iduser = %s", (user_id_str,))
                self.conn.commit()
                print(f"\n✅ SUCESSO: Usuário '{nome}' foi deletado. Seus papéis foram removidos em cascata.")
            except psycopg2.IntegrityError:
                self.conn.rollback()
                print(f"❌ ERRO: Não foi possível deletar. O usuário '{nome}' ainda possui outros vínculos (entregas, grupos, etc.). Remova-os primeiro.")
        else:
            print("Operação de deleção cancelada.")
    
    # --- 2. Gerenciamento de Matrículas ---
    def submenu_matriculas(self):
        while True:
            print("\n--- 🎓 Gerenciamento de Matrículas ---")
            print("1. Matricular Aluno em Disciplina")
            print("2. Vincular Professor a Disciplina")
            print("3. Vincular Monitor a Disciplina")
            print("4. Voltar ao Menu Principal")

            escolha = input("Escolha uma opção: ")
            if escolha == '1': self.vincular_usuario_disciplina('aluno')
            elif escolha == '2': self.vincular_usuario_disciplina('professor')
            elif escolha == '3': self.vincular_usuario_disciplina('monitor')
            elif escolha == '4': break
            else: print("❌ Opção inválida.")
            if escolha in ['1', '2', '3']: self._press_enter_to_continue()
    
    def vincular_usuario_disciplina(self, papel):
        print(f"\n--- Vincular {papel.capitalize()} a uma Disciplina ---")
        self.listar_usuarios(prompt=False)
        user_id = input(f"\nDigite o ID do Usuário para vincular como {papel}: ")
        self.listar_disciplinas()
        codigo_disc = input("\nDigite o código da disciplina: ")

        nome_usuario, _ = self._get_user_info(user_id)
        nome_disciplina = self._get_discipline_name(codigo_disc)
        if nome_usuario == "Usuário Desconhecido" or nome_disciplina == "Disciplina Desconhecida":
            print("❌ Usuário ou Disciplina não encontrado.")
            return
            
        try:
            user_id_int = int(user_id)
            self.cur.execute(sql.SQL("SELECT 1 FROM {} WHERE iduser = %s").format(sql.Identifier(papel)), (user_id_int,))
            if not self.cur.fetchone():
                print(f"❌ ERRO: O usuário {nome_usuario} não possui o papel de {papel}. Vá ao menu de usuários para adicioná-lo.")
                return

            tabela_juncao = {'aluno': 'alunodisc', 'professor': 'profdisc', 'monitor': 'monitdisc'}[papel]
            query = sql.SQL("INSERT INTO {} (iduser, codigodisc) VALUES (%s, %s)").format(sql.Identifier(tabela_juncao))
            self.cur.execute(query, (user_id_int, codigo_disc))
            self.conn.commit()
            print(f"\n✅ SUCESSO: {papel.capitalize()} '{nome_usuario}' vinculado à disciplina '{nome_disciplina}'.")
        except psycopg2.errors.UniqueViolation:
            self.conn.rollback()
            print("❌ ERRO: Este usuário já está vinculado a esta disciplina com este papel.")
        except (ValueError, TypeError):
            print("❌ ID de usuário inválido.")
        except Exception as e:
            self.conn.rollback()
            print(f"❌ ERRO Inesperado: {e}")

    # --- 3. Gerenciamento de Disciplinas e Conteúdos ---
    def gerenciar_disciplinas(self):
        while True:
            print("\n--- 📚 Gerenciamento de Disciplinas e Conteúdos ---")
            print("1. Criar Nova Disciplina")
            print("2. Adicionar Conteúdo a uma Disciplina")
            print("3. Voltar ao Menu Principal")
            
            escolha = input("Escolha uma opção: ")
            if escolha == '1': self.criar_disciplina()
            elif escolha == '2': self.submenu_conteudo()
            elif escolha == '3': break
            else: print("❌ Opção inválida.")
            if escolha in ['1', '2']: self._press_enter_to_continue()

    def criar_disciplina(self):
        print("\n--- Criar Nova Disciplina ---")
        codigo = input("Código da Disciplina (ex: 2025-1-BD-01): ")
        nome = input("Nome da Disciplina: ")
        periodo = input("Período (ex: 2025.1): ")
        foto = input("Caminho da Foto (opcional): ") or 'default.jpg'
        query = "INSERT INTO disciplina (codigodisc, nomedisc, periododisc, fotodisc) VALUES (%s, %s, %s, %s)"
        try:
            self.cur.execute(query, (codigo, nome, periodo, foto))
            self.conn.commit()
            print(f"\n✅ SUCESSO: Disciplina '{nome}' criada com o código '{codigo}'.")
        except psycopg2.errors.UniqueViolation:
            self.conn.rollback()
            print(f"❌ ERRO: Já existe uma disciplina com o código '{codigo}'.")

    def submenu_conteudo(self):
        self.listar_disciplinas()
        codigo_disc = input("\nDigite o código da disciplina para adicionar conteúdo: ")
        if self._get_discipline_name(codigo_disc) == "Disciplina Desconhecida":
            print("❌ Código de disciplina inválido.")
            return

        while True:
            print(f"\n--- ➕ Adicionando Conteúdo em '{self._get_discipline_name(codigo_disc)}' ---")
            print("1. Adicionar Módulo")
            print("2. Adicionar Tópico a um Módulo")
            print("3. Adicionar Atividade")
            print("4. Adicionar Questionário")
            print("5. Voltar")

            escolha = input("Escolha o tipo de conteúdo: ")
            if escolha == '1': self.adicionar_modulo(codigo_disc)
            elif escolha == '2': self.adicionar_topico(codigo_disc)
            elif escolha == '3': self.adicionar_atividade(codigo_disc)
            elif escolha == '4': self.adicionar_questionario(codigo_disc)
            elif escolha == '5': break
            else: print("❌ Opção inválida.")
            if escolha in ['1', '2', '3', '4']: self._press_enter_to_continue()

    def adicionar_modulo(self, codigo_disc):
        print("\n--- Adicionar Novo Módulo ---")
        nome_modulo = input("Nome do Módulo: ")
        modulo_id = self._get_next_id('modulo', 'idmodulo')
        query = "INSERT INTO modulo (idmodulo, nomemodulo, codigodisc) VALUES (%s, %s, %s)"
        self.cur.execute(query, (modulo_id, nome_modulo, codigo_disc))
        self.conn.commit()
        print(f"\n✅ SUCESSO: Módulo '{nome_modulo}' (ID: {modulo_id}) adicionado.")

    def adicionar_topico(self, codigo_disc):
        self.cur.execute("SELECT idmodulo, nomemodulo FROM modulo WHERE codigodisc = %s", (codigo_disc,))
        modulos = self.cur.fetchall()
        if not modulos:
            print("❌ ERRO: Nenhum módulo encontrado. Crie um módulo primeiro.")
            return
            
        print("\n--- Módulos Disponíveis ---")
        for mod in modulos: print(f"ID: {mod[0]}, Nome: {mod[1]}")
        
        try:
            modulo_id = int(input("Digite o ID do módulo para adicionar o tópico: "))
            nome_topico = input("Nome do Tópico: ")
            conteudo = input("Conteúdo do Tópico: ")
            topico_id = self._get_next_id('topico', 'idtopico')
            
            query = "INSERT INTO topico (idtopico, nometopico, conteudotopico, idmodulo) VALUES (%s, %s, %s, %s)"
            self.cur.execute(query, (topico_id, nome_topico, conteudo, modulo_id))
            self.conn.commit()
            print(f"\n✅ SUCESSO: Tópico '{nome_topico}' (ID: {topico_id}) adicionado.")
        except (ValueError, TypeError):
            print("❌ ID do módulo inválido.")
            self.conn.rollback()

    def adicionar_atividade(self, codigo_disc):
        try:
            print("\n--- Adicionar Nova Atividade ---")
            nome = input("Nome da Atividade: ")
            tipo = input("Tipo (Individual/Grupo): ").capitalize()
            prazo = input("Prazo (AAAA-MM-DD): ")
            pont_max_str = input("Pontuação Máxima (opcional, ex: 10.0): ")
            pont_max = float(pont_max_str) if pont_max_str else None
            id_categ = None

            if tipo == 'Grupo':
                self.cur.execute("SELECT idcateg, nomecateg FROM categoria_de_grupo WHERE codigodisc = %s", (codigo_disc,))
                categorias = self.cur.fetchall()
                if not categorias:
                    print("❌ ERRO: Nenhuma categoria de grupo nesta disciplina. Crie uma no menu de grupos.")
                    return
                print("\n--- Categorias de Grupo Disponíveis ---")
                for cat in categorias: print(f"ID: {cat[0]}, Nome: {cat[1]}")
                id_categ = int(input("Digite o ID da categoria para esta atividade de grupo: "))

            atividade_id = self._get_next_id('atividade', 'idativ')
            query = "INSERT INTO atividade (idativ, nomeativ, tipoativ, prazoativ, pontmaxativ, codigodisc, idcateg) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            self.cur.execute(query, (atividade_id, nome, tipo, prazo, pont_max, codigo_disc, id_categ))
            self.conn.commit()
            print(f"\n✅ SUCESSO: Atividade '{nome}' (ID: {atividade_id}) criada.")
        except (ValueError, TypeError):
            print("❌ ERRO: Pontuação ou ID de categoria inválido.")
            self.conn.rollback()
        
    def adicionar_questionario(self, codigo_disc):
        try:
            print("\n--- Adicionar Novo Questionário ---")
            nome = input("Nome do Questionário: ")
            prazo = input("Prazo (AAAA-MM-DD): ")
            num_tentativas = int(input("Número de Tentativas: "))
            perguntas = input("Caminho do arquivo de Perguntas (ex: perguntas.json): ")
            
            questionario_id = self._get_next_id('questionario', 'idquest')
            query = "INSERT INTO questionario (idquest, nomequest, prazoquest, numtentaquest, perguntasquest, codigodisc) VALUES (%s, %s, %s, %s, %s, %s)"
            self.cur.execute(query, (questionario_id, nome, prazo, num_tentativas, perguntas, codigo_disc))
            self.conn.commit()
            print(f"\n✅ SUCESSO: Questionário '{nome}' (ID: {questionario_id}) criado.")
        except (ValueError, TypeError):
            print("❌ ERRO: Número de tentativas deve ser um número inteiro.")
            self.conn.rollback()

    # --- 4. Gerenciamento de Entregas e Notas ---
    def gerenciar_entregas(self):
        while True:
            print("\n--- 📝 Gerenciamento de Entregas e Notas ---")
            print("1. Registrar Entrega de Atividade")
            print("2. Registrar Tentativa de Questionário")
            print("3. Lançar/Atualizar Notas")
            print("4. Voltar ao Menu Principal")

            escolha = input("Escolha uma opção: ")
            if escolha == '1': self.registrar_entrega_atividade()
            elif escolha == '2': self.registrar_tentativa_questionario()
            elif escolha == '3': self.submenu_atualizar_notas()
            elif escolha == '4': break
            else: print("❌ Opção inválida.")
            if escolha in ['1', '2', '3']: self._press_enter_to_continue()
            
    def registrar_entrega_atividade(self):
        print("\n--- Registrar Entrega de Atividade ---")
        self.cur.execute("SELECT idativ, nomeativ, tipoativ, codigodisc FROM atividade ORDER BY nomeativ")
        atividades = self.cur.fetchall()
        if not atividades:
            print("Nenhuma atividade encontrada.")
            return

        print("\n--- Atividades Disponíveis ---")
        for atv in atividades:
            print(f"ID: {atv[0]}, Nome: {atv[1]}, Tipo: {atv[2]}, Disciplina: {self._get_discipline_name(atv[3])}")
        
        id_ativ_str = input("\nDigite o ID da atividade: ")
        
        nome_ativ, tipo_ativ = self._get_activity_info(id_ativ_str)
        if nome_ativ == "Atividade Desconhecida":
            print("❌ Atividade não encontrada.")
            return
            
        conteudo = input("Conteúdo da Entrega (ex: link do GitHub, caminho do arquivo): ")
        data_entrega = datetime.now().strftime('%Y-%m-%d')
        entrega_id = self._get_next_id('entrega_de_atividade', 'identatv')
        id_user = None
        id_grupo = None
        
        try:
            if tipo_ativ.lower() == 'individual':
                id_user_str = input("Digite o ID do aluno que está entregando: ")
                nome_aluno, _ = self._get_user_info(id_user_str)
                if nome_aluno == "Usuário Desconhecido":
                    print("❌ Aluno não encontrado.")
                    return
                id_user = int(id_user_str)
                print(f"Registrando entrega de '{nome_aluno}' para '{nome_ativ}'.")
            else: # Grupo
                id_grupo_str = input("Digite o ID do grupo que está entregando: ")
                id_grupo = int(id_grupo_str)
                print(f"Registrando entrega do Grupo ID {id_grupo} para '{nome_ativ}'.")

            query = "INSERT INTO entrega_de_atividade (identatv, conteudoentatv, dataentatv, idativ, idgrupo, iduser) VALUES (%s, %s, %s, %s, %s, %s)"
            self.cur.execute(query, (entrega_id, conteudo, data_entrega, int(id_ativ_str), id_grupo, id_user))
            self.conn.commit()
            print(f"\n✅ SUCESSO: Entrega registrada com ID {entrega_id}.")
        except (ValueError, TypeError):
            print("❌ ERRO: ID inválido.")
            self.conn.rollback()
        except Exception as e:
            self.conn.rollback()
            print(f"❌ ERRO ao registrar entrega: {e}")

    def registrar_tentativa_questionario(self):
        print("\n--- Registrar Tentativa de Questionário ---")
        self.cur.execute("SELECT idquest, nomequest, codigodisc FROM questionario ORDER BY nomequest")
        questionarios = self.cur.fetchall()
        if not questionarios:
            print("Nenhum questionário encontrado.")
            return

        print("\n--- Questionários Disponíveis ---")
        for q in questionarios: print(f"ID: {q[0]}, Nome: {q[1]}, Disciplina: {self._get_discipline_name(q[2])}")
        
        try:
            id_quest = int(input("\nDigite o ID do questionário: "))
            id_user = int(input("Digite o ID do aluno: "))
            respostas = input("Caminho para o arquivo de respostas (ex: resp.json): ")
            data_tentativa = datetime.now().strftime('%Y-%m-%d')
            tentativa_id = self._get_next_id('tentativa_de_questionario', 'idtentquest')
            
            query = "INSERT INTO tentativa_de_questionario (idtentquest, resptentquest, datatentquest, idquest, iduser) VALUES (%s, %s, %s, %s, %s)"
            self.cur.execute(query, (tentativa_id, respostas, data_tentativa, id_quest, id_user))
            self.conn.commit()
            nome_aluno, _ = self._get_user_info(id_user)
            print(f"\n✅ SUCESSO: Tentativa de '{nome_aluno}' (ID: {tentativa_id}) registrada.")
        except (ValueError, TypeError):
            print("❌ ERRO: IDs devem ser números.")
            self.conn.rollback()
        except Exception as e:
            self.conn.rollback()
            print(f"❌ ERRO ao registrar tentativa: {e}")

    def submenu_atualizar_notas(self):
        print("\n--- Lançar/Atualizar Notas ---")
        print("1. Notas de Atividades")
        print("2. Notas de Questionários")
        escolha = input("Escolha o que deseja avaliar: ")
        
        try:
            if escolha == '1':
                self.cur.execute("""
                    SELECT e.identatv, a.nomeativ, COALESCE(u.primnomeuser || ' ' || u.sobrenomeuser, 'Grupo ID: ' || g.idgrupo) as entregue_por, e.notaentatv
                    FROM entrega_de_atividade e
                    JOIN atividade a ON e.idativ = a.idativ
                    LEFT JOIN usuario u ON e.iduser = u.iduser
                    LEFT JOIN grupo g ON e.idgrupo = g.idgrupo
                    ORDER BY e.dataentatv DESC
                """)
                entregas = self.cur.fetchall()
                if not entregas:
                    print("Nenhuma entrega de atividade encontrada.")
                    return
                print("\n--- Entregas para Avaliação ---")
                for e in entregas: print(f"ID Entrega: {e[0]}, Atividade: {e[1]}, Por: {e[2]}, Nota Atual: {e[3] or 'Pendente'}")
                
                entrega_id = int(input("\nDigite o ID da entrega para lançar/atualizar a nota: "))
                nota = float(input("Digite a nova nota: "))
                
                self.cur.execute("UPDATE entrega_de_atividade SET notaentatv = %s WHERE identatv = %s", (nota, entrega_id))
            elif escolha == '2':
                self.cur.execute("""
                    SELECT t.idtentquest, q.nomequest, u.primnomeuser, u.sobrenomeuser, t.notatentquest
                    FROM tentativa_de_questionario t
                    JOIN questionario q ON t.idquest = q.idquest
                    JOIN usuario u ON t.iduser = u.iduser
                    ORDER BY t.datatentquest DESC
                """)
                tentativas = self.cur.fetchall()
                if not tentativas:
                    print("Nenhuma tentativa de questionário encontrada.")
                    return
                print("\n--- Tentativas para Avaliação ---")
                for t in tentativas: print(f"ID Tentativa: {t[0]}, Questionário: {t[1]}, Aluno: {t[2]} {t[3]}, Nota Atual: {t[4] or 'Pendente'}")

                tentativa_id = int(input("\nDigite o ID da tentativa para lançar/atualizar a nota: "))
                nota = float(input("Digite a nova nota: "))

                self.cur.execute("UPDATE tentativa_de_questionario SET notatentquest = %s WHERE idtentquest = %s", (nota, tentativa_id))
            else:
                print("❌ Opção inválida.")
                return

            self.conn.commit()
            print("\n✅ SUCESSO: Nota atualizada.")
        except (ValueError, TypeError):
            print("❌ ERRO: ID ou nota inválida. Devem ser números.")
            self.conn.rollback()
        except Exception as e:
            print(f"❌ ERRO: {e}")
            self.conn.rollback()

    # --- 5. Gerenciamento de Grupos ---
    def gerenciar_grupos(self):
        while True:
            print("\n--- 👨‍👩‍👧‍👦 Gerenciamento de Grupos ---")
            print("1. Criar Categoria de Grupo em uma Disciplina")
            print("2. Criar Novo Grupo")
            print("3. Adicionar Aluno a um Grupo")
            print("4. Listar Grupos e seus Membros")
            print("5. Voltar ao Menu Principal")
            
            escolha = input("Escolha uma opção: ")
            if escolha == '1': self.criar_categoria_grupo()
            elif escolha == '2': self.criar_grupo()
            elif escolha == '3': self.adicionar_aluno_grupo()
            elif escolha == '4': self.listar_grupos()
            elif escolha == '5': break
            else: print("❌ Opção inválida.")
            if escolha in ['1', '2', '3', '4']: self._press_enter_to_continue()
    
    def criar_categoria_grupo(self):
        self.listar_disciplinas()
        codigo_disc = input("\nDigite o código da disciplina para a nova categoria: ")
        if self._get_discipline_name(codigo_disc) == "Disciplina Desconhecida":
            print("❌ Código de disciplina inválido.")
            return
        
        nome_categ = input("Nome da Categoria (ex: 'Seminários', 'Projeto Final'): ")
        categoria_id = self._get_next_id('categoria_de_grupo', 'idcateg')
        
        query = "INSERT INTO categoria_de_grupo (idcateg, nomecateg, codigodisc) VALUES (%s, %s, %s)"
        self.cur.execute(query, (categoria_id, nome_categ, codigo_disc))
        self.conn.commit()
        
        disc_name = self._get_discipline_name(codigo_disc)
        print(f"\n✅ SUCESSO: Categoria de grupo '{nome_categ}' criada para a disciplina '{disc_name}'.")

    def criar_grupo(self):
        self.cur.execute("SELECT c.idcateg, c.nomecateg, d.nomedisc FROM categoria_de_grupo c JOIN disciplina d ON c.codigodisc = d.codigodisc")
        categorias = self.cur.fetchall()
        if not categorias:
            print("❌ ERRO: Nenhuma categoria de grupo encontrada. Crie uma categoria primeiro.")
            return
            
        print("\n--- Categorias de Grupo Disponíveis ---")
        for cat in categorias: print(f"ID: {cat[0]}, Categoria: {cat[1]}, Disciplina: {cat[2]}")
        
        try:
            categoria_id = int(input("\nDigite o ID da categoria para o novo grupo: "))
            nome_grupo = input("Nome do Grupo: ")
            limite = int(input("Limite de Membros: "))
            grupo_id = self._get_next_id('grupo', 'idgrupo')
            
            query = "INSERT INTO grupo (idgrupo, nomegrupo, limitusersgrupo, idcateg) VALUES (%s, %s, %s, %s)"
            self.cur.execute(query, (grupo_id, nome_grupo, limite, categoria_id))
            self.conn.commit()
            print(f"\n✅ SUCESSO: Grupo '{nome_grupo}' (ID: {grupo_id}) foi criado.")
        except (ValueError, TypeError):
            print("❌ ERRO: ID ou limite inválido. Devem ser números.")
            self.conn.rollback()

    def adicionar_aluno_grupo(self):
        self.listar_grupos()
        try:
            grupo_id_str = input("\nDigite o ID do grupo para adicionar um aluno: ")
            grupo_id = int(grupo_id_str)
            
            # Checar se o grupo existe
            self.cur.execute("SELECT 1 FROM grupo WHERE idgrupo = %s", (grupo_id,))
            if not self.cur.fetchone():
                print("❌ Grupo não encontrado.")
                return

            self.cur.execute("""
                SELECT u.iduser, u.primnomeuser, u.sobrenomeuser FROM usuario u 
                JOIN alunodisc ad ON u.iduser = ad.iduser
                JOIN categoria_de_grupo c ON ad.codigodisc = c.codigodisc
                JOIN grupo g ON c.idcateg = g.idcateg
                WHERE g.idgrupo = %s AND u.iduser NOT IN (SELECT iduser FROM alunogrupo WHERE idgrupo = %s)
            """, (grupo_id, grupo_id))
            alunos = self.cur.fetchall()
            
            if not alunos:
                print("Nenhum aluno elegível (matriculado na disciplina e fora do grupo) encontrado.")
                return
                
            print("\n--- Alunos Disponíveis para o Grupo ---")
            for aluno in alunos: print(f"ID: {aluno[0]}, Nome: {aluno[1]} {aluno[2]}")
            
            aluno_id_str = input("Digite o ID do aluno a ser adicionado: ")
            aluno_id = int(aluno_id_str)
            
            query = "INSERT INTO alunogrupo (iduser, idgrupo) VALUES (%s, %s)"
            self.cur.execute(query, (aluno_id, grupo_id))
            self.conn.commit()
            aluno_nome, _ = self._get_user_info(aluno_id)
            print(f"\n✅ SUCESSO: Aluno '{aluno_nome}' adicionado ao grupo ID {grupo_id}.")
        except (ValueError, TypeError):
            print("❌ ERRO: IDs devem ser números.")
            self.conn.rollback()
        except psycopg2.errors.UniqueViolation:
            self.conn.rollback()
            print("❌ ERRO: Este aluno já está neste grupo.")
        except Exception as e:
            self.conn.rollback()
            print(f"❌ ERRO: {e}")

    def listar_grupos(self):
        self.cur.execute("""
            SELECT g.idgrupo, g.nomegrupo, c.nomecateg, d.nomedisc,
                   (SELECT COUNT(*) FROM alunogrupo WHERE idgrupo = g.idgrupo), g.limitusersgrupo
            FROM grupo g JOIN categoria_de_grupo c ON g.idcateg = c.idcateg
            JOIN disciplina d ON c.codigodisc = d.codigodisc
            ORDER BY d.nomedisc, c.nomecateg, g.nomegrupo
        """)
        grupos = self.cur.fetchall()
        
        print("\n--- 👥 Lista de Grupos e Membros ---")
        if not grupos:
            print("Nenhum grupo encontrado.")
            return

        for grupo in grupos:
            print(f"\nID Grupo: {grupo[0]} | Nome: {grupo[1]} | Membros: {grupo[4]}/{grupo[5]}")
            print(f"  Disciplina: {grupo[3]} | Categoria: {grupo[2]}")
            
            self.cur.execute("SELECT u.iduser, u.primnomeuser, u.sobrenomeuser FROM alunogrupo ag JOIN usuario u ON ag.iduser = u.iduser WHERE ag.idgrupo = %s", (grupo[0],))
            membros = self.cur.fetchall()
            
            if membros:
                print("  Membros:")
                for membro in membros: print(f"    - ID: {membro[0]}, Nome: {membro[1]} {membro[2]}")
            else:
                print("  (Nenhum membro neste grupo)")

    # --- 6. Gerenciamento de Mensagens ---
    def submenu_mensagens(self):
        while True:
            print("\n--- 📨 Gerenciamento de Mensagens ---")
            print("1. Enviar Mensagem para Alunos de uma Disciplina")
            print("2. Ver Mensagens Recebidas por um Usuário")
            print("3. Voltar ao Menu Principal")
            
            escolha = input("Escolha uma opção: ")
            if escolha == '1': self.enviar_mensagem()
            elif escolha == '2': self.ver_mensagens()
            elif escolha == '3': break
            else: print("❌ Opção inválida.")
            if escolha in ['1', '2']: self._press_enter_to_continue()
            
    def enviar_mensagem(self):
        print("\n--- Enviar Nova Mensagem ---")
        self.listar_usuarios(prompt=False)
        try:
            sender_id = int(input("Digite o ID do remetente: "))
            self.listar_disciplinas()
            codigo_disc = input("Digite o código da disciplina para enviar a mensagem aos alunos: ")

            self.cur.execute("SELECT u.iduser FROM usuario u JOIN alunodisc ad ON u.iduser = ad.iduser WHERE ad.codigodisc = %s", (codigo_disc,))
            alunos = self.cur.fetchall()
            if not alunos:
                print("Nenhum aluno encontrado nesta disciplina.")
                return

            conteudo = input("\nDigite o conteúdo da mensagem: ")
            msg_id = self._get_next_id('mensagem', 'idmsg')
            data_envio = datetime.now().strftime('%Y-%m-%d')
            
            self.cur.execute("INSERT INTO mensagem (idmsg, conteudomsg, dataenviomsg, iduser) VALUES (%s, %s, %s, %s)", (msg_id, conteudo, data_envio, sender_id))
            recipients = [(aluno[0], msg_id) for aluno in alunos]
            self.cur.executemany("INSERT INTO userrecebmsg (iduser, idmsg) VALUES (%s, %s)", recipients)
            
            self.conn.commit()
            sender_name, _ = self._get_user_info(sender_id)
            disc_name = self._get_discipline_name(codigo_disc)
            print(f"\n✅ SUCESSO: Mensagem de '{sender_name}' enviada para {len(recipients)} aluno(s) da disciplina '{disc_name}'.")
        except (ValueError, TypeError):
            print("❌ ERRO: ID do remetente inválido.")
            self.conn.rollback()

    def ver_mensagens(self):
        print("\n--- Ver Mensagens Recebidas ---")
        self.listar_usuarios(prompt=False)
        try:
            user_id = int(input("Digite o ID do usuário para ver suas mensagens: "))
            
            query = """
            SELECT m.dataenviomsg, u.primnomeuser, u.sobrenomeuser, m.conteudomsg
            FROM mensagem m JOIN userrecebmsg urm ON m.idmsg = urm.idmsg
            JOIN usuario u ON m.iduser = u.iduser
            WHERE urm.iduser = %s ORDER BY m.dataenviomsg DESC
            """
            self.cur.execute(query, (user_id,))
            mensagens = self.cur.fetchall()
            
            user_name, _ = self._get_user_info(user_id)
            print(f"\n--- ✉️ Mensagens para {user_name} ---")
            if not mensagens:
                print("Nenhuma mensagem encontrada.")
                return
                
            for msg in mensagens:
                print(f"Data: {msg[0]} | De: {msg[1]} {msg[2]} | Mensagem: {msg[3]}")
        except (ValueError, TypeError):
            print("❌ ERRO: ID do usuário inválido.")

    # --- 7. Módulo de Relatórios ---
    def submenu_relatorios(self):
        while True:
            print("\n--- 📊 Módulo de Relatórios ---")
            print("1. Gerar Boletim de Notas do Aluno por Disciplina")
            print("2. Gerar Lista de Alunos por Disciplina")
            print("3. Visualizar Vínculos de um Usuário com Disciplinas")
            print("4. Visualizar Membros da Disciplina por Papel")
            print("5. Voltar ao Menu Principal")
            
            escolha = input("Escolha uma opção de relatório: ")
            if escolha == '1': self.gerar_boletim_aluno()
            elif escolha == '2': self.gerar_lista_alunos_disciplina()
            elif escolha == '3': self.visualizar_vinculos_usuario()
            elif escolha == '4': self.visualizar_membros_disciplina()
            elif escolha == '5': break
            else: print("❌ Opção inválida.")
            if escolha in ['1', '2', '3', '4']: self._press_enter_to_continue()

    def visualizar_membros_disciplina(self):
        """Lista todos os professores, monitores e alunos de uma disciplina."""
        print("\n--- Visualizar Membros da Disciplina ---")
        self.listar_disciplinas()
        codigo_disc = input("\nDigite o código da disciplina para ver seus membros: ")
        nome_disciplina = self._get_discipline_name(codigo_disc)
        if nome_disciplina == "Disciplina Desconhecida":
            print("❌ Código de disciplina inválido.")
            return

        print("\n" + "="*60)
        print(f"👥 MEMBROS DA DISCIPLINA: {nome_disciplina.upper()}")
        print("="*60)

        # Professores
        self.cur.execute("SELECT u.iduser, u.primnomeuser, u.sobrenomeuser FROM usuario u JOIN profdisc pd ON u.iduser = pd.iduser WHERE pd.codigodisc = %s ORDER BY u.primnomeuser", (codigo_disc,))
        professores = self.cur.fetchall()
        print("\n--- 👨‍🏫 Professores ---")
        if not professores:
            print("(Nenhum professor vinculado)")
        else:
            for p in professores: print(f"ID: {p[0]} | Nome: {p[1]} {p[2]}")

        # Monitores
        self.cur.execute("SELECT u.iduser, u.primnomeuser, u.sobrenomeuser FROM usuario u JOIN monitdisc md ON u.iduser = md.iduser WHERE md.codigodisc = %s ORDER BY u.primnomeuser", (codigo_disc,))
        monitores = self.cur.fetchall()
        print("\n--- 🧑‍🏫 Monitores ---")
        if not monitores:
            print("(Nenhum monitor vinculado)")
        else:
            for m in monitores: print(f"ID: {m[0]} | Nome: {m[1]} {m[2]}")

        # Alunos
        self.cur.execute("SELECT u.iduser, u.primnomeuser, u.sobrenomeuser, a.matriculaaluno FROM usuario u JOIN aluno a ON u.iduser = a.iduser JOIN alunodisc ad ON a.iduser = ad.iduser WHERE ad.codigodisc = %s ORDER BY u.primnomeuser", (codigo_disc,))
        alunos = self.cur.fetchall()
        print("\n--- 👨‍🎓 Alunos ---")
        if not alunos:
            print("(Nenhum aluno matriculado)")
        else:
            for a in alunos: print(f"ID: {a[0]} | Nome: {a[1]} {a[2]} | Matrícula: {a[3]}")
        print("="*60)

    def visualizar_vinculos_usuario(self):
        """Lista todas as disciplinas e os respectivos papéis de um usuário específico."""
        print("\n--- Visualizar Vínculos de um Usuário com Disciplinas ---")
        self.listar_usuarios(prompt=False)
        try:
            user_id = int(input("\nDigite o ID do usuário para ver seus vínculos: "))
            nome_usuario, _ = self._get_user_info(user_id)
            if nome_usuario == "Usuário Desconhecido":
                print("❌ ID de usuário não encontrado.")
                return
        except (ValueError, TypeError):
            print("❌ ID inválido.")
            return

        query = """
        SELECT d.nomedisc, 'Aluno' as papel
        FROM alunodisc ad
        JOIN disciplina d ON ad.codigodisc = d.codigodisc
        WHERE ad.iduser = %s
        UNION ALL
        SELECT d.nomedisc, 'Professor' as papel
        FROM profdisc pd
        JOIN disciplina d ON pd.codigodisc = d.codigodisc
        WHERE pd.iduser = %s
        UNION ALL
        SELECT d.nomedisc, 'Monitor' as papel
        FROM monitdisc md
        JOIN disciplina d ON md.codigodisc = d.codigodisc
        WHERE md.iduser = %s
        ORDER BY nomedisc, papel;
        """
        self.cur.execute(query, (user_id, user_id, user_id))
        vinculos = self.cur.fetchall()
        
        print("\n" + "="*60)
        print(f"🔗 Vínculos para: {nome_usuario} (ID: {user_id})")
        print("="*60)
        
        if not vinculos:
            print("Este usuário não está vinculado a nenhuma disciplina.")
        else:
            print(f"{'Disciplina':<45} | {'Papel':<15}")
            print("-" * 60)
            for disciplina, papel in vinculos:
                print(f"{disciplina:<45} | {papel:<15}")
        print("="*60)

    def gerar_boletim_aluno(self):
        print("\n--- Gerar Boletim do Aluno ---")
        self.listar_disciplinas()
        codigo_disc = input("\nDigite o código da disciplina: ")
        
        try:
            self.cur.execute("SELECT u.iduser, u.primnomeuser, u.sobrenomeuser, a.matriculaaluno FROM usuario u JOIN aluno a ON u.iduser = a.iduser JOIN alunodisc ad ON u.iduser = ad.iduser WHERE ad.codigodisc = %s ORDER BY u.primnomeuser", (codigo_disc,))
            alunos = self.cur.fetchall()
            if not alunos:
                print("❌ Nenhum aluno matriculado nesta disciplina.")
                return

            print("\n--- Alunos Matriculados ---")
            for aluno in alunos: print(f"ID: {aluno[0]}, Nome: {aluno[1]} {aluno[2]}, Matrícula: {aluno[3]}")
            aluno_id = int(input("\nDigite o ID do aluno para gerar o boletim: "))

            nome_aluno, matricula_aluno = self._get_user_info(aluno_id)
            nome_disciplina = self._get_discipline_name(codigo_disc)
            
            print("\n" + "="*50)
            print(f"📊 BOLETIM DO ALUNO")
            print(f"Aluno: {nome_aluno} (Matrícula: {matricula_aluno})")
            print(f"Disciplina: {nome_disciplina}")
            print("="*50)

            # Notas de Atividades
            self.cur.execute("SELECT a.nomeativ, e.notaentatv, a.pontmaxativ FROM entrega_de_atividade e JOIN atividade a ON e.idativ = a.idativ WHERE (e.iduser = %s OR e.idgrupo IN (SELECT idgrupo FROM alunogrupo WHERE iduser = %s)) AND a.codigodisc = %s", (aluno_id, aluno_id, codigo_disc))
            notas_atividades = self.cur.fetchall()
            
            total_obtidos, total_possiveis = 0.0, 0.0
            print("\n--- Notas de Atividades ---")
            if not notas_atividades:
                print("Nenhuma nota de atividade encontrada.")
            else:
                for nome, nota, pontmax in notas_atividades:
                    nota_str = f"{nota:.2f}" if nota is not None else "Pendente"
                    pontmax_str = f"{pontmax:.2f}" if pontmax is not None else "N/A"
                    print(f"  - {nome}: {nota_str} / {pontmax_str}")
                    if nota: total_obtidos += nota
                    if pontmax: total_possiveis += pontmax

            # Notas de Questionários
            self.cur.execute("SELECT q.nomequest, t.notatentquest, q.pontmaxquest FROM tentativa_de_questionario t JOIN questionario q ON t.idquest = q.idquest WHERE t.iduser = %s AND q.codigodisc = %s", (aluno_id, codigo_disc))
            notas_questionarios = self.cur.fetchall()
            print("\n--- Notas de Questionários ---")
            if not notas_questionarios:
                print("Nenhuma nota de questionário encontrada.")
            else:
                for nome, nota, pontmax in notas_questionarios:
                    nota_str = f"{nota:.2f}" if nota is not None else "Pendente"
                    pontmax_str = f"{pontmax:.2f}" if pontmax is not None else "N/A"
                    print(f"  - {nome}: {nota_str} / {pontmax_str}")
                    if nota: total_obtidos += nota
                    if pontmax: total_possiveis += pontmax
            
            print("\n--- Resumo ---")
            if total_possiveis > 0:
                percentual = (total_obtidos / total_possiveis) * 100
                print(f"Total de Pontos Obtidos: {total_obtidos:.2f}")
                print(f"Total de Pontos Possíveis: {total_possiveis:.2f}")
                print(f"Aproveitamento: {percentual:.2f}%")
            else:
                print("Não há atividades com pontuação definida.")
            print("="*50)
        except (ValueError, TypeError):
            print("❌ ERRO: ID do aluno deve ser um número.")

    def gerar_lista_alunos_disciplina(self):
        print("\n--- Gerar Lista de Alunos por Disciplina ---")
        self.listar_disciplinas()
        codigo_disc = input("\nDigite o código da disciplina: ")
        nome_disciplina = self._get_discipline_name(codigo_disc)
        if nome_disciplina == "Disciplina Desconhecida":
            print("❌ Código de disciplina inválido.")
            return
        
        self.cur.execute("SELECT a.matriculaaluno, u.primnomeuser, u.sobrenomeuser FROM usuario u JOIN aluno a ON u.iduser = a.iduser JOIN alunodisc ad ON u.iduser = ad.iduser WHERE ad.codigodisc = %s ORDER BY u.primnomeuser, u.sobrenomeuser;", (codigo_disc,))
        alunos = self.cur.fetchall()

        print("\n" + "="*60)
        print(f"👨‍🎓 LISTA DE ALUNOS - {nome_disciplina.upper()}")
        print("="*60)
        
        if not alunos:
            print("Nenhum aluno matriculado encontrado.")
        else:
            print(f"{'Matrícula':<15} | {'Nome Completo':<40}")
            print("-" * 60)
            for matricula, prim_nome, sobrenome in alunos:
                print(f"{matricula:<15} | {f'{prim_nome} {sobrenome}':<40}")
        print("="*60)
        print(f"Total de Alunos: {len(alunos)}")
        print("="*60)

    def listar_disciplinas(self):
        self.cur.execute("SELECT codigodisc, nomedisc, periododisc FROM disciplina ORDER BY nomedisc")
        disciplinas = self.cur.fetchall()
        print("\n--- 📚 Lista de Disciplinas Disponíveis ---")
        if not disciplinas:
            print("Nenhuma disciplina encontrada.")
            return []
        for disc in disciplinas:
            print(f"Código: {disc[0]} | Nome: {disc[1]} | Período: {disc[2]}")
        return disciplinas

    # --- Menu Principal ---
    def menu_principal(self):
        """Exibe o menu principal da aplicação."""
        while True:
            print("\n" + "="*15 + " SISTEMA eClass - MENU PRINCIPAL " + "="*15)
            print("1. 👤 Gerenciar Usuários")
            print("2. 🎓 Gerenciar Matrículas")
            print("3. 📚 Gerenciar Disciplinas e Conteúdos")
            print("4. 📝 Gerenciar Entregas e Notas")
            print("5. 👨‍👩‍👧‍👦 Gerenciar Grupos")
            print("6. 📨 Enviar e Ver Mensagens")
            print("7. 📊 Gerar Relatórios")
            print("8. 🛠️ Ferramentas de Desenvolvedor")
            print("9. 🚪 Sair")
            
            escolha = input("Escolha uma opção: ")
            
            if escolha == '1': self.submenu_usuarios()
            elif escolha == '2': self.submenu_matriculas()
            elif escolha == '3': self.gerenciar_disciplinas()
            elif escolha == '4': self.gerenciar_entregas()
            elif escolha == '5': self.gerenciar_grupos()
            elif escolha == '6': self.submenu_mensagens()
            elif escolha == '7': self.submenu_relatorios()
            elif escolha == '8': self.submenu_dev()
            elif escolha == '9':
                self.disconnect()
                break
            else:
                print("❌ Opção inválida. Tente novamente.")

    # --- Ferramentas de Desenvolvedor ---
    def submenu_dev(self):
        while True:
            print("\n--- 🛠️ Ferramentas de Desenvolvedor ---")
            print("1. Analisar por ID de Usuário")
            print("2. Analisar por Nome de Usuário")
            print("3. Voltar ao Menu Principal")
            escolha = input("Escolha uma opção: ")

            if escolha == '1':
                self.executar_analise_por_id()
            elif escolha == '2':
                self.executar_analise_por_nome()
            elif escolha == '3':
                break
            else:
                print("❌ Opção inválida.")
            self._press_enter_to_continue()
    
    def executar_analise_por_id(self):
        try:
            user_id = int(input("Digite o ID do usuário para analisar a consulta de vínculos: "))

            # Desabilitar uso de índices para forçar seq scan
            self.cur.execute("SET enable_indexscan = OFF;")
            self.cur.execute("SET enable_bitmapscan = OFF;")
            self.cur.execute("SET enable_tidscan = OFF;")

            print("🛑 Desabilitando uso de índices para primeira análise...")

            query = """
            EXPLAIN ANALYZE
            SELECT d.nomedisc, 'Aluno' as papel
            FROM alunodisc ad
            JOIN disciplina d ON ad.codigodisc = d.codigodisc
            WHERE ad.iduser = %s
            UNION ALL
            SELECT d.nomedisc, 'Professor' as papel
            FROM profdisc pd
            JOIN disciplina d ON pd.codigodisc = d.codigodisc
            WHERE pd.iduser = %s
            UNION ALL
            SELECT d.nomedisc, 'Monitor' as papel
            FROM monitdisc md
            JOIN disciplina d ON md.codigodisc = d.codigodisc
            WHERE md.iduser = %s
            ORDER BY nomedisc, papel
            """
            params = (user_id, user_id, user_id)
            self.cur.execute(query, params)

            print("\n📊 EXPLAIN ANALYZE sem índice:")
            for row in self.cur.fetchall():
                linha = row[0]
                if "Execution Time" in linha:
                    print(linha)

            # Restaurar uso de índices
            self.cur.execute("SET enable_indexscan = ON;")
            self.cur.execute("SET enable_bitmapscan = ON;")
            self.cur.execute("SET enable_tidscan = ON;")

            print("\n⚙️ Criando índices temporários nas colunas iduser...")
            self.cur.execute("CREATE INDEX idx_temp_alunodisc_iduser ON alunodisc(iduser);")
            self.cur.execute("CREATE INDEX idx_temp_profdisc_iduser ON profdisc(iduser);")
            self.cur.execute("CREATE INDEX idx_temp_monitdisc_iduser ON monitdisc(iduser);")

            self.cur.execute(query, params)
            print("\n📊 EXPLAIN ANALYZE com índices:")
            for row in self.cur.fetchall():
                linha = row[0]
                if "Execution Time" in linha:
                    print(linha)

            print("\n▶️ Executando consulta de verdade:")
            self.cur.execute(query.replace("EXPLAIN ANALYZE", ""), params)
            resultados = self.cur.fetchall()
            print(f"\n🔍 Vínculos encontrados para o usuário ID {user_id}:")
            for disc, papel in resultados:
                print(f"Disciplina: {disc}, Papel: {papel}")

            print("\n🗑️ Removendo índices temporários...")
            self.cur.execute("DROP INDEX IF EXISTS idx_temp_alunodisc_iduser;")
            self.cur.execute("DROP INDEX IF EXISTS idx_temp_profdisc_iduser;")
            self.cur.execute("DROP INDEX IF EXISTS idx_temp_monitdisc_iduser;")

        except (ValueError, TypeError):
            print("❌ ID de usuário inválido.")
        except Exception as e:
            print(f"❌ Ocorreu um erro: {e}")

    def executar_analise_por_nome(self):
        """
        Busca e exibe os dados da tabela 'usuario' filtrando exatamente pelo primeiro nome.
        Garante que não exista índice antes da primeira medição, cria índice para segunda, executa consulta e apaga índice.
        """
        try:
            nome_busca = input("Digite o primeiro nome do usuário para buscar: ")
            if not nome_busca:
                print("❌ Nome não pode ser vazio.")
                return

            param_explain = (nome_busca,)
            query = """
            SELECT iduser, primnomeuser, sobrenomeuser, fotouser, datanascuser, cidadeuser, estadouser, paisuser
            FROM usuario
            WHERE primnomeuser = %s
            """

            # Apagar índice se existir, para garantir que não tenha índice na primeira medição
            try:
                self.cur.execute("DROP INDEX IF EXISTS idx_temp_primnomeuser;")
                self.conn.commit()
                print("🗑️ Índice temporário apagado antes da primeira medição.")
            except Exception as e:
                print(f"⚠️ Não foi possível apagar índice antes da medição: {e}")

            print("\n📊 EXPLAIN ANALYZE sem índice:")
            self.cur.execute("EXPLAIN ANALYZE " + query, param_explain)
            explain_before = self.cur.fetchall()
            for linha in explain_before:
                if "Execution Time" in linha[0]:
                    print(linha[0])

            print("\n⚙️ Criando índice temporário...")
            self.cur.execute("CREATE INDEX idx_temp_primnomeuser ON usuario (primnomeuser);")
            self.conn.commit()

            print("\n📊 EXPLAIN ANALYZE com índice:")
            self.cur.execute("EXPLAIN ANALYZE " + query, param_explain)
            explain_after = self.cur.fetchall()
            for linha in explain_after:
                if "Execution Time" in linha[0]:
                    print(linha[0])

            print("\n▶️ Executando consulta de verdade:")
            self.cur.execute(query, param_explain)
            usuarios = self.cur.fetchall()

            if not usuarios:
                print(f"❌ Nenhum usuário encontrado com o nome '{nome_busca}'.")
            else:
                print(f"\n🔍 Usuários encontrados com nome exatamente '{nome_busca}':")
                for u in usuarios:
                    print(f"ID: {u[0]}, Nome: {u[1]} {u[2]}, Data Nasc: {u[4]}, Cidade: {u[5]}, Estado: {u[6]}, País: {u[7]}")

            print("\n🗑️ Removendo índice temporário...")
            self.cur.execute("DROP INDEX IF EXISTS idx_temp_primnomeuser;")
            self.conn.commit()

        except Exception as e:
            print(f"❌ Ocorreu um erro: {e}")




if __name__ == "__main__":
    try:
        sistema = EClassCRUD()
        sistema.menu_principal()
    except (psycopg2.OperationalError, psycopg2.InterfaceError) as db_error:
        print(f"\n❌ ERRO DE CONEXÃO: Não foi possível conectar ao banco de dados. Verifique a conexão e as credenciais.")
        print(f"Detalhe do erro: {db_error}")
    except KeyboardInterrupt:
        print("\n\nOperação interrompida pelo usuário. Encerrando o programa.")
    except Exception as e:
        print(f"❌ Ocorreu um erro fatal inesperado no sistema: {e}")
    finally:
        print("\nPrograma finalizado.")
