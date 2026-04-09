-- Querie to access to mpersona_sarlaft table
SELECT
    /* id */
    id_persona,

    /* CIIU */
    cod_ciiu,

    /* ocupation code */
    cod_ocupacion,

    /* job */
    desc_cargo,

    /* income */
    imp_ingreso,
    imp_otr_ingreso,
    desc_otr_ingreso,

    /* expenses */
    imp_egreso,

    /* assets */
    imp_activo,

    /* liabilities */
    imp_pasivo
    
FROM mpersona_sarlaft