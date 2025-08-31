let spec = null;

export async function loadSpec() {
  const resp = await fetch("/openapi.json");
  spec = await resp.json();
  return spec;
}

export function getSpec() {
  return spec;
}

export function discoverRollEndpoints() {
  if (!spec) throw new Error("Spec not loaded");
  const endpoints = [];

  for (const [path, methods] of Object.entries(spec.paths)) {
    if (!path.match(/\/api\/v\d+\//)) continue;

    const method = methods.get ? "GET" : methods.post ? "POST" : null;
    if (!method) continue;

    const operation = methods.get || methods.post;
    if (!operation.tags || !operation.tags.includes("rolls")) continue;

    const name = path.split("/").pop();
    const params = [];

    if (method === "GET" && operation.parameters) {
      for (const p of operation.parameters) {
        if (p.in === "query" && p.schema && p.schema.type === "integer") {
          params.push({ name: p.name, required: p.required || false });
        }
      }
    }

    let bodyColors = null;
    if (method === "POST" && operation.requestBody) {
      const content = operation.requestBody.content;
      const jsonSchema =
        content &&
        content["application/json"] &&
        content["application/json"].schema;
      if (jsonSchema && jsonSchema.additionalProperties) {
        const schemas = spec.components && spec.components.schemas;
        if (schemas) {
          for (const s of Object.values(schemas)) {
            if (s.enum && s.type === "string") {
              bodyColors = s.enum;
              break;
            }
          }
        }
      }
    }

    endpoints.push({
      path,
      method,
      name,
      params,
      bodyColors,
      operationId: operation.operationId,
    });
  }

  return endpoints;
}

export async function createRoom() {
  const resp = await fetch("/api/v1/room", { method: "POST" });
  return resp.json();
}

export async function getRolls(roomUid, seqId) {
  const url = "/api/v1/room/" + roomUid + "?seq_id=" + seqId;
  const resp = await fetch(url);
  return resp.json();
}

export async function submitRoll(endpoint, roomUid, userName, params) {
  const headers = {
    "X-Room": roomUid,
    "X-User-Name": userName,
  };

  if (endpoint.method === "GET") {
    const query = new URLSearchParams();
    for (const [key, value] of Object.entries(params)) {
      if (value !== undefined && value !== 0) query.set(key, String(value));
    }
    const url = endpoint.path + "?" + query.toString();
    const resp = await fetch(url, { headers });
    return resp.json();
  }

  if (endpoint.method === "POST") {
    headers["Content-Type"] = "application/json";
    const resp = await fetch(endpoint.path, {
      method: "POST",
      headers,
      body: JSON.stringify(params),
    });
    return resp.json();
  }
}
