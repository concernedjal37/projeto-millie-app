create database Banco_da_Millie;
use Banco_da_Millie;

create table Usuarios(
id int unsigned primary key  not null auto_increment,
nome varchar(100) not null,
e_mail varchar(100) not null,
foto varchar(50)
);
create table Telefones_usuario(
telefone char(5)
);
create table Configuracoes_usuario(
modo_escuro boolean
);