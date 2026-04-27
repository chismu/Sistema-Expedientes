
const API_URL = "http://127.0.0.1:8000";

export const getExpedientes = async () => {
    const res = await fetch(`${API_URL}/expedientes/`);
    return res.json();
};

export const crearExpediente = async (data) => {
    const res = await fetch(`${API_URL}/expedientes/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    return res.json();
};

export const getPersonas = async () => {
    const res = await fetch(`${API_URL}/personas/`);
    return res.json();
};

export const asignarExpediente = async (id, persona_id) => {
    const res = await fetch(`${API_URL}/expedientes/${id}/asignar?persona_id=${persona_id}`, {
        method: "PUT",
    });
    return res.json();
};

export const finalizarExpediente = async (id) => {
    const res = await fetch(`${API_URL}/expedientes/${id}/finalizar`, {
        method: "PUT",
    });
    return res.json();
};

export default API;
