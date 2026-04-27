import { useEffect, useState } from "react";
import { crearExpediente, getPersonas } from "../api/api";

export default function ExpedienteForm({ onCreated }) {
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

        await crearExpediente({
            ...form,
            persona_id: Number(form.persona_id)
        });

        // limpiar form
        setForm({
            numero_expediente: "",
            caratula: "",
            fecha_ingreso: "",
            persona_id: ""
        });

        // refrescar tabla
        if (onCreated) onCreated();
    };

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

            <button className="btn btn-primary">
                Crear Expediente
            </button>
        </form>
    );
}