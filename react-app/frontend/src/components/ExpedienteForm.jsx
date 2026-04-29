import { useEffect, useState } from "react";
import { crearExpediente, getPersonas } from "../api/api";

export default function ExpedienteForm({ expediente, onCreated }) {

    const [personas, setPersonas] = useState([]);

    const [form, setForm] = useState({
        numero_expediente: "",
        caratula: "",
        fecha_ingreso: "",
        persona_id: ""
    });

    useEffect(() => {
        const cargar = async () => {
            const data = await getPersonas();
            setPersonas(data);
        };
        cargar();
    }, []);

    const handleChange = (e) => {
        setForm({
            ...form,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (expediente) {
            // 🔥 EDITAR
            await fetch(`http://127.0.0.1:8000/expedientes/${expediente.id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(form)
            });
        } else {
            // 🔥 CREAR
            await crearExpediente({
                ...form,
                persona_id: Number(form.persona_id)
            });
        }

        // limpiar
        setForm({
            numero_expediente: "",
            caratula: "",
            fecha_ingreso: "",
            persona_id: ""
        });

        if (onCreated) onCreated();
    };

    useEffect(() => {
        if (expediente) {
            setForm(expediente);
        }
    }, [expediente]);

    return (
        <form onSubmit={handleSubmit} className="card p-3 mb-4">
            <h5>Nuevo Expediente</h5>

            <input
                className="form-control mb-2"
                name="numero_expediente"
                placeholder="Número"
                value={form.numero_expediente}
                onChange={handleChange}
                required
            />

            <input
                className="form-control mb-2"
                name="caratula"
                placeholder="Carátula"
                value={form.caratula}
                onChange={handleChange}
                required
            />

            <input
                type="date"
                className="form-control mb-2"
                name="fecha_ingreso"
                value={form.fecha_ingreso}
                onChange={handleChange}
                required
            />

            <select
                className="form-select mb-2"
                name="persona_id"
                value={form.persona_id}
                onChange={handleChange}
                required
            >
                <option value="">Seleccionar persona</option>
                {personas.map((p) => (
                    <option key={p.id} value={p.id}>
                        {p.nombre}
                    </option>
                ))}
            </select>
            <input
                className="form-control mb-2"
                name="estado"
                placeholder="Estado"
                value={form.estado || ""}
                onChange={handleChange}
            />

            <input
                className="form-control mb-2"
                name="tipo"
                placeholder="Tipo"
                value={form.tipo || ""}
                onChange={handleChange}
            />

            <input
                type="date"
                className="form-control mb-2"
                name="fecha_limite"
                value={form.fecha_limite || ""}
                onChange={handleChange}
            />

            <textarea
                className="form-control mb-2"
                name="accion"
                placeholder="Acción"
                value={form.accion || ""}
                onChange={handleChange}
            />

            <textarea
                className="form-control mb-2"
                name="observaciones"
                placeholder="Observaciones"
                value={form.observaciones || ""}
                onChange={handleChange}
            />

            <button className="btn btn-primary">
                Crear Expediente
            </button>

        </form>
    );
}