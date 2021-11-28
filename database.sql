create database if not exists taller3;
use taller3;

create table entrenador(
	username text primary key,
	password text not null,
	nombre text not null,
	apellido text not null,
	edad int not null,
	fecha_nacimiento date not null
);

create table tipo (
	id_tipo serial primary key,
	nombre text not null unique,
	id_tipo_fortaleza int default null references tipo(id_tipo),
	id_tipo_debilidad int default null references tipo(id_tipo)
);

create table ataque (
	nombre_ataque text primary key,
	id_tipo int not null references tipo(id_tipo),
	base_damage int not null
);

create table especie (
	id_especie serial primary key,
	nombre_especie text not null unique,
	id_tipo1 int not null references tipo(id_tipo),
	id_tipo2 int default null references tipo(id_tipo)
);

create table equipo_lucha (
	id_equipo serial primary key,
	username_entrenador text not null references entrenador(username)
);

create table monstruo (
	id_monstruo serial primary key,
	id_equipo int not null references equipo_lucha(id_equipo),
	id_especie int not null references especie(id_especie),
	posicion_equipo int not null,
	puntos_salud int not null,
	velocidad int not null,
	nombre_ataque1 text not null references ataque(nombre_ataque),
	nombre_ataque2 text default null references ataque(nombre_ataque),
	nombre_ataque3 text default null references ataque(nombre_ataque),
	nombre_ataque4 text default null references ataque(nombre_ataque)
);

create table creatudex (
	id_creatudex serial primary key,
	username_entrenador text not null references entrenador(username)
);

create table especies_registradas (
	id_especie int not null references especie(id_especie),
	id_creatudex int not null references creatudex(id_creatudex)
);

create table lucha (
	username_ganador text not null references entrenador(username),
	username_perdedor text not null references entrenador(username)
);