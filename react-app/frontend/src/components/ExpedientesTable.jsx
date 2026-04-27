import { useEffect, useState } from "react";
import { 
    getExpedientes, 
    finalizarExpediente, 
    asignarExpediente, 
    getPersonas 
} from "../api/api";

export default function ExpedientesTable() {
    const [expedientes, setExpedientes] = useState([]);
    const [personas, setPersonas] = useState([]);

    const cargar = async () => {
        const data = await getExpedientes();
        setExpedientes(data);
    };

    const cargarPersonas = async () => {
        const data = await getPersonas();
        setPersonas(data);
    };

    useEffect(() => {
        cargar();
        cargarPersonas();
    }, []);

    const getColorClass = (color) => {
        if (color === "rojo") return "table-danger";
        if (color === "amarillo") return "table-warning";
        return "table-success";
    };

    const finalizar = async (id) => {
        await finalizarExpediente(id);
        cargar();
    };

    const asignar = async (id, persona_id) => {
        if (!persona_id) return;
        await asignarExpediente(id, persona_id);
        cargar();
    };

    return (
        <table className="table table-bordered">
            <thead>
                <tr>
                    <th>N°</th>
                    <th>Carátula</th>
                    <th>Días</th>
                    <th>Estado</th>
                    <th>Asignar</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                {expedientes.map((e) => (
                    <tr key={e.id} className={getColorClass(e.color)}>
                        <td>{e.numero}</td>
                        <td>{e.caratula}</td>
                        <td>{e.dias_sin_mover}</td>
                        <td>
                            <span className="badge bg-dark">
                                {e.color.toUpperCase()}
                            </span>
                        </td>

                        {/* SELECT PERSONAS */}
                        <td>
                            <select
                                className="form-select"
                                onChange={(ev) =>
                                    asignar(e.id, ev.target.value)
                                }
                            >
                                <option value="">Asignar...</option>
                                {personas.map((p) => (
                                    <option key={p.id} value={p.id}>
                                        {p.nombre}
                                    </option>
                                ))}
                            </select>
                        </td>

                        {/* BOTONES */}
                        <td>
                            <button
                                className="btn btn-danger btn-sm"
                                onClick={() => finalizar(e.id)}
                            >
                                Finalizar
                            </button>
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
}