-- Querie to access to mpersona table
SELECT 
    /* id */
    id_persona,

    /* Name */
    txt_nombre,
    txt_apellido1,
    txt_apellido2,

    /* ID */
    cod_tipo_doc,
    nro_doc,
    nro_nit,
    fec_exp_cedula, 
    
    /* Birth_date */
    fec_nac,

    /* Gender */
    txt_sexo,

    /* Birth_place */
    txt_lugar_nac,
    cod_pais_nac,
    cod_dpto_nac,
    cod_municipio_nac,

    /* Civil state */
    cod_est_civil  


FROM mpersona;
