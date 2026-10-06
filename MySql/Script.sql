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
valor float not null,
plataforma varchar(50) not null
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
status_gerais varchar(20),
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

create table Tranferencia_bonificada(
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

#drop database Banco_da_Millie;