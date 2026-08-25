export function getDatabaseConfig(env = process.env) {
  return {
    uri: env.DB_URI || "bolt://localhost:7687",
    username: env.DB_USERNAME || "",
    password: env.DB_PASSWORD || ""
  };
}

export function getServerConfig(env = process.env) {
  return {
    port: Number(env.PORT) || 9000,
    host: env.HOST || "0.0.0.0"
  };
}