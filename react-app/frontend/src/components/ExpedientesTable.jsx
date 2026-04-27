import { useEffect, useState } from "react";
import { getExpedientes, finalizarExpediente } from "../api/api";

export default function ExpedientesTable() {
    const [expedientes, setExpedientes] = useState([]);

    const cargar = async () => {
        const data = await getExpedientes();
        setExpedientes(data);
    };

    useEffect(() => {
        cargar();
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

    return (
        <table className="table">
            <thead>
                <tr>
                    <th>Número</th>
                    <th>Carátula</th>
                    <th>Días</th>
                    <th>Estado</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                {expedientes.map((e) => (
                    <tr key={e.id} className={getColorClass(e.color)}>
                        <td>{e.numero}</td>
                        <td>{e.caratula}</td>
                        <td>{e.dias_sin_mover}</td>
                        <td>{e.color}</td>
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