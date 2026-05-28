DROP DATABASE estatisticas_dnd;
CREATE DATABASE estatisticas_dnd;
USE estatisticas_dnd;

CREATE TABLE tamanhos (
	id INT PRIMARY KEY AUTO_INCREMENT,
    tamanho VARCHAR(25) NOT NULL
);

CREATE TABLE tipos (
	id INT PRIMARY KEY AUTO_INCREMENT,
    tipo VARCHAR(25)
);

CREATE TABLE subtipos (
	id INT PRIMARY KEY AUTO_INCREMENT,
    subtipo VARCHAR(25)
);

CREATE TABLE alinhamentos (
	id INT PRIMARY KEY AUTO_INCREMENT,
    alinhamento VARCHAR(25)
);

CREATE TABLE deslocamentos (
	id INT PRIMARY KEY AUTO_INCREMENT,
    deslocamento VARCHAR(25)
);

CREATE TABLE pericias (
	id INT PRIMARY KEY AUTO_INCREMENT,
    pericia VARCHAR(25)
);

CREATE TABLE resistencias (
	id INT PRIMARY KEY AUTO_INCREMENT,
    resistencia VARCHAR(25)
);

CREATE TABLE vulnerabilidades (
	id INT PRIMARY KEY AUTO_INCREMENT,
    vulnerabilidade VARCHAR(25)
);

CREATE TABLE imunidades_dano (
	id INT PRIMARY KEY AUTO_INCREMENT,
    imunidade VARCHAR(25)
);

CREATE TABLE imunidades_condicao (
	id INT PRIMARY KEY AUTO_INCREMENT,
    imunidade VARCHAR(25)
);

CREATE TABLE sentidos (
	id INT PRIMARY KEY AUTO_INCREMENT,
    sentido VARCHAR(30)
);

CREATE TABLE idiomas (
	id INT PRIMARY KEY AUTO_INCREMENT,
    idioma VARCHAR(25)
);

CREATE TABLE habitats (
	id INT PRIMARY KEY AUTO_INCREMENT,
    habitat VARCHAR(25)
);

CREATE TABLE monstros (
	id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(150),
    tipo_id INT,
    FOREIGN KEY (tipo_id) REFERENCES tipos(id),
    subtipo_id INT,
    FOREIGN KEY (subtipo_id) REFERENCES subtipos(id),
    classe_armadura INT,
    pontos_vida INT,
    forca INT,
    destreza INT,
    constituicao INT,
    inteligencia INT,
    sabedoria INT,
    carisma INT,
    nivel_desafio VARCHAR(25),
    fonte VARCHAR(150)
);

CREATE TABLE deslocamento_monstro (
	id INT PRIMARY KEY AUTO_INCREMENT,
    deslocamento_id INT,
    FOREIGN KEY (deslocamento_id) REFERENCES deslocamentos(id),
    monstro_id INT,
    FOREIGN KEY (monstro_id) REFERENCES monstros(id),
    distancia INT
);

CREATE TABLE pericia_monstro (
	id INT PRIMARY KEY AUTO_INCREMENT,
    pericia_id INT,
    FOREIGN KEY (pericia_id) REFERENCES pericias(id),
    monstro_id INT,
    FOREIGN KEY (monstro_id) REFERENCES monstros(id)
);

CREATE TABLE alinhamento_monstro (
	id INT PRIMARY KEY AUTO_INCREMENT,
    alinhamento_id INT,
    FOREIGN KEY (alinhamento_id) REFERENCES alinhamentos(id),
    monstro_id INT,
    FOREIGN KEY (monstro_id) REFERENCES monstros(id)
);

CREATE TABLE resistencia_monstro (
	id INT PRIMARY KEY AUTO_INCREMENT,
    resistencia_id INT,
    FOREIGN KEY (resistencia_id) REFERENCES resistencias(id),
    monstro_id INT,
    FOREIGN KEY (monstro_id) REFERENCES monstros(id)
);

CREATE TABLE vulnerabilidade_monstro (
	id INT PRIMARY KEY AUTO_INCREMENT,
    vulnerabilidade_id INT,
    FOREIGN KEY (vulnerabilidade_id) REFERENCES vulnerabilidades(id),
    monstro_id INT,
    FOREIGN KEY (monstro_id) REFERENCES monstros(id)
);

CREATE TABLE imunidade_dano_monstro (
	id INT PRIMARY KEY AUTO_INCREMENT,
    imunidade_id INT,
    FOREIGN KEY (imunidade_id) REFERENCES imunidades_dano(id),
    monstro_id INT,
    FOREIGN KEY (monstro_id) REFERENCES monstros(id)
);

CREATE TABLE imunidade_condicao_monstro (
	id INT PRIMARY KEY AUTO_INCREMENT,
    imunidade_id INT,
    FOREIGN KEY (imunidade_id) REFERENCES imunidades_condicao(id),
    monstro_id INT,
    FOREIGN KEY (monstro_id) REFERENCES monstros(id)
);

CREATE TABLE sentido_monstro (
	id INT PRIMARY KEY AUTO_INCREMENT,
    sentido_id INT,
    FOREIGN KEY (sentido_id) REFERENCES sentidos(id),
    monstro_id INT,
    FOREIGN KEY (monstro_id) REFERENCES monstros(id),
    distancia INT
);

CREATE TABLE idioma_monstro (
	id INT PRIMARY KEY AUTO_INCREMENT,
    idioma_id INT,
    FOREIGN KEY (idioma_id) REFERENCES idiomas(id),
    monstro_id INT,
    FOREIGN KEY (monstro_id) REFERENCES monstros(id)
);

CREATE TABLE habitat_monstro (
	id INT PRIMARY KEY AUTO_INCREMENT,
    habitat_id INT,
    FOREIGN KEY (habitat_id) REFERENCES habitats(id),
    monstro_id INT,
    FOREIGN KEY (monstro_id) REFERENCES monstros(id)
);

CREATE TABLE tamanho_monstro (
	id INT PRIMARY KEY AUTO_INCREMENT,
    tamanho_id INT,
    FOREIGN KEY (tamanho_id) REFERENCES tamanhos(id),
    monstro_id INT,
    FOREIGN KEY (monstro_id) REFERENCES monstros(id)
);