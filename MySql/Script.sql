#Se você quiser criar o banco todo de uma vez compilando todas as linhas infelizmente será necessario você ler um dos comentarios localizado na linha 160. Se estiver no vscode utilize Crtl + G para ir deretamente para a linha
#Comandos para a criação do banco por si só
create database Banco_da_Millie;
use Banco_da_Millie;

create table Usuarios(
id int unsigned primary key not null auto_increment,
nome varchar(100) not null,
e_mail varchar(100) not null,
cep char(9),
bairro varchar(50),
cidade varchar(50),
estado varchar(25),
pais varchar(20)
)ENGINE = InnoDB;
#drop table Usuarios;

create table Telefones_usuario(
id_usuario int unsigned not null,
telefone char(9) not null,
foreign key (id_usuario) references usuarios(id)
)ENGINE = InnoDB;
#drop table Telefones_usuario;

create table Configuracoes_usuario(
id_usuario int unsigned not null,
modo_escuro boolean,
foto varchar(50),
foreign key(id_usuario) references usuarios(id)
)ENGINE = InnoDB;
#drop table Configuracoes_usuario;

create table cotacoes(
id int unsigned primary key not null auto_increment,
valor_min float not null,
valor_max float not null,
plataforma varchar(50) not null,
agencia varchar(20) not null
)ENGINE = InnoDB;
#drop table cotacoes;

create table Historico_de_cotacoes(
id_usuarios int unsigned not null,
id_cotacoes int unsigned not null,
ultima_data_atualizacao datetime,
favorito boolean,
constraint primary key(id_usuarios, id_cotacoes),
foreign key(id_usuarios) references usuarios(id),
foreign key(id_cotacoes) references cotacoes(id)
)ENGINE = InnoDB;
#drop table Historico_de_cotacoes;

create table Promocoes(
id int unsigned primary key not null auto_increment,
link varchar(500) not null,
data_limite datetime not null,
plataforma_de_origem varchar(20) not null
)ENGINE = InnoDB;
#drop table Promocoes;

create table historico_de_promocoes(
id_promocoes int unsigned not null,
id_usuarios int unsigned not null,
ultima_data_atualizacao datetime,
favorito boolean,
constraint primary key(id_promocoes, id_usuarios),
foreign key(id_promocoes) references promocoes(id),
foreign key(id_usuarios) references usuarios(id)
)ENGINE = InnoDB;
#drop table historico_de_promocoes;

create table Transferencia_bonificada(
id_promocoes int unsigned not null,
plataforma_de_destino varchar(20) not null,
percentual_MAX float not null,
percentual_MIN float not null,
foreign key(id_promocoes) references promocoes(id)
)ENGINE = InnoDB;
#drop table Tranferencia_bonificada;

create table Compra_bonificada(
id_promocoes int unsigned not null,
percentual_MAX float not null,
percentual_MIN float not null,
foreign key(id_promocoes) references promocoes(id)
)ENGINE = InnoDB;
#drop table Compra_bonificada;

create table Adesao_bonificada(
id_promocoes int unsigned not null,
quantidade_milhas int not null,
foreign key(id_promocoes) references promocoes(id)
)ENGINE = InnoDB;
#drop table Adesao_bonificada;

create table Viagens(
id int unsigned primary key not null auto_increment,
categoiria varchar(45) not null,
origem varchar(50) not null,
destino varchar(50) not null,
data_ida datetime not null,
data_volta datetime not null,
numero_adultos int not null,
numero_criacas int not null,
numero_bebes int not null
)ENGINE = InnoDB;
#drop table Viagens;

create table Historico_de_pesquisa(
id_viagens int unsigned not null,
id_usuarios int unsigned not null,
data_pesquisa datetime,
favorito boolean,
constraint primary key(id_viagens, id_usuarios),
foreign key(id_viagens) references viagens(id),
foreign key(id_usuarios) references usuarios(id)
)ENGINE = InnoDB;
#drop table Historico_de_pesquisa;

create table Rota(
id int unsigned primary key not null auto_increment,
id_viagens int unsigned not null,
tipo varchar(15) not null,
aeroporto_origem varchar(50) not null,
aeroporto_destino varchar(50) not null,
quantidade_paradas int not null,
foreign key(id_viagens) references viagens(id)
)ENGINE = InnoDB;
#drop table Rota;

create table Oferta(
codigo int primary key not null,
id_rota int unsigned not null,
companhia_aerea varchar(25) not null,
provedora_viagem varchar(25) not null,
preco_milhas float not null,
preco_moeda float not null,
classe varchar(10) not null,
link varchar(500) not null,
foreign key(id_rota) references rota(id)
)ENGINE = InnoDB;
#drop table Oferta;

#Tabela para informar erros aos programadores
create table log_operacoes(
id int primary key not null auto_increment,
descricao_acao varchar(500) not null,
variavel_1 varchar(10),
variavel_2 varchar(10),
variavel_3 varchar(10),
variavel_4 varchar(10),
variavel_5 varchar(10)
)ENGINE = InnoDB;
#drop table log_operacoes;

#drop database Banco_da_Millie;

#Componentes do banco de dados
#	Procedures
#Tenha em vista que essa sintaxe foi feita no mariadb então não ira funcionar tudo de uma vez(no caso compilar todas as linhas) a partir daqui!
#Criar cotações
DELIMITER //
create procedure criar_cota(IN plat varchar(50), IN val_min float, IN val_max float, IN agen varchar(20))
begin
declare repeticoes int;
set repeticoes = (select count(*) from cotacoes where agencia = agen);
	if repeticoes = 0 then
		#se a cotação não existe
		insert into cotacoes (valor_min, plataforma, valor_max, agencia) values (val_min, plat, val_max, agen);
	else
		#se existe então troca para o novo valor caso sejá igual
		update cotacoes set valor_min = val_min, valor_max = val_max where plataforma = plat and valor_min != val_min and valor_max != val_max;
	end if;
end //
DELIMITER ;
#call criar_cota(plataforma, valor minimo, valor maximo, agencia);
#drop procedure criar_cota;

#Criar promoções
DELIMITER //
create procedure adicionar_promo(
in link varchar(500), in plataforma_de_origem varchar(20), in data_limite datetime, in codigo_verificacao tinyint,
in plat_destino varchar(20) default 'ND', in percent_max float default 0, in percent_min float default 0,
in quant_milhas int default 0
)
begin
declare novo_id int;
if codigo_verificacao not between 1 and 3 then
	#Caso o código esteja errado
	insert into log_operacoes(descricao_acao) values('Erro: Código Back_End digitou o código errado');
	select descricao_acao from log_operacoes;
else
	#Insere a promoção
	insert into Promocoes(link, data_limite, plataforma_de_origem) values(link, data_limite, plataforma_de_origem);
	#Pega o id
	set novo_id = (select id from Promocoes order by id desc limit 1);
	#Switch case de chernobyl
	case codigo_verificacao
		#Transferencia Bonificada
		when 1 then
			insert into Transferencia_bonificada(id_promocoes, plataforma_de_destino, percentual_MAX, percentual_MIN) values(novo_id, plat_destino, percent_max, percent_min);
			#Insere no Log para informar da operação
			insert into log_operacoes(descricao_acao) values('Operação de inserção de Transferencia Bonificada feita');
		#Compra Bonificada
		when 2 then
			insert into Compra_bonificada(id_promocoes, percentual_MAX, percentual_MIN) values(novo_id, percent_max, percent_min);
			#Insere no Log para informar da operação
			insert into log_operacoes(descricao_acao) values('Operação de inserção de Compra Bonificada feita');
		#Adesão Bonificada
		when 3 then
			insert into Adesao_bonificada(id_promocoes, quantidade_milhas) values(novo_id, quant_milhas);
			#Insere no Log para informar da operação
			insert into log_operacoes(descricao_acao) values('Operação de inserção de Adesão Bonificada feita');
			end case;
end if;
end //
DELIMITER ;
#drop procedure adicionar_promo;
#Eu darei um exemplo de uso melhor depois, ainda não sei com total certeza como funciona os argumentos opcionais e eles ainda precisam de uma configuração melhor talvez
#call adicionar_promo('akljfbsjkdjk', 'Smiles', data e hora,3);

#Functions
#Não criado ainda
#	Views
#View para visualização melhor dos desenvolvedores(ou talvez poderia ser utilizado de outras formas também) em relação a todos os dados de um tipo.
create or replace view Verificar_Transferencia_Boni as select * from Promocoes join Transferencia_bonificada on id = id_promocoes;
#select * from Verificar_Transferencia_Boni;
create or replace view Verificar_Compra_Boni as select * from Promocoes join Compra_bonificada on id = id_promocoes;
#select * from Verificar_Compra_Boni;
create or replace view Verificar_Adesao_Boni as select * from Promocoes join Adesao_bonificada on id = id_promocoes;
#select * from Verificar_Adesao_Boni;
