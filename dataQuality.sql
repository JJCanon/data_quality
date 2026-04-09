/* 
======================================================
Modelo de Evaluación de Calidad de Datos
Tablas: Tabla, Campo, Dimension, Ejecucion, Resultado
======================================================
*/

USE data_process;
GO

-- Table: Tabla
CREATE TABLE dbo.Tabla (
    id      INT IDENTITY(1,1)   NOT NULL CONSTRAINT PK_Tabla PRIMARY KEY,
    tabla   VARCHAR(128)        NOT NULL
);
GO
CREATE UNIQUE INDEX UX_Tabla_tabla ON dbo.Tabla(tabla);
GO

-- Table: Campo
CREATE TABLE dbo.Campo (
    id          INT IDENTITY(1,1)   NOT NULL CONSTRAINT PK_Campo PRIMARY KEY,
    id_tabla    INT                 NOT NULL,
    campo       VARCHAR(128)        NOT NULL,
    CONSTRAINT FK_Campo_Tabla FOREIGN KEY (id_tabla) REFERENCES dbo.Tabla(id)
);
GO
CREATE UNIQUE INDEX UX_Campo_tabla_campo ON dbo.Campo(id_tabla, campo);
GO

-- Table: Dimension
CREATE TABLE dbo.Dimension (
    id          INT IDENTITY(1,1)   NOT NULL CONSTRAINT PK_Dimension PRIMARY KEY,
    dimension   VARCHAR(64)         NOT NULL              
);
GO
CREATE UNIQUE INDEX UX_Dimension_dimension ON dbo.Dimension(dimension);
GO

-- Table: Ejecucion
CREATE TABLE dbo.Ejecucion (
    id                  INT IDENTITY(1,1)   NOT NULL CONSTRAINT PK_Ejecucion PRIMARY KEY,  
    fecha_ejecucion     DATETIME            NOT NULL CONSTRAINT DF_Ejecucion_fecha DEFAULT (GETDATE()),
    fuente              VARCHAR(255)        NULL,
    notas               VARCHAR(MAX)        NULL                                            
);
GO

-- Table: Resultado
CREATE TABLE dbo.Resultado (
    id                  INT IDENTITY(1,1)   NOT NULL CONSTRAINT PK_Resultado PRIMARY KEY,
    id_ejecucion        INT                 NOT NULL,
    id_campo            INT                 NOT NULL,
    id_dimension        INT                 NOT NULL,
    score               DECIMAL(10,4)       NOT NULL,

    CONSTRAINT FK_Resultado_Ejecucion  FOREIGN KEY (id_ejecucion)  REFERENCES dbo.Ejecucion(id),
    CONSTRAINT FK_Resultado_Campo      FOREIGN KEY (id_campo)       REFERENCES dbo.Campo(id),     
    CONSTRAINT FK_Resultado_Dimension  FOREIGN KEY (id_dimension)   REFERENCES dbo.Dimension(id)
);
GO
CREATE UNIQUE INDEX UX_Resultado_exec_campo_dim ON dbo.Resultado(id_ejecucion, id_campo, id_dimension);
GO