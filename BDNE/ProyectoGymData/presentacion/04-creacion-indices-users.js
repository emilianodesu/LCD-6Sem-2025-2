// Índice único en email
db.users.createIndex({ email: 1 }, { unique: true });
// Índice geoespacial para buscar usuarios por ubicación (targets the nested field)
db.users.createIndex({ "direccion.ubicacion": "2dsphere" });
