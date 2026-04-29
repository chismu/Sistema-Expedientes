import { useEffect, useState } from "react";
import { getEstadisticas } from "../api/api";

export default function Estadisticas() {
    const [data, setData] = useState([]);

    useEffect(() => {
        const cargar = async () => {
            const res = await getEstadisticas();
            setData(res);
        };
        cargar();
    }, []);

    return (
        <div className="mt-4">
            <h4>Estadísticas por Persona</h4>

            <table className="table table-bordered">
                <thead>
                    <tr>
                        <th>Persona</th>
                        <th>Expedientes</th>
                        <th>Total</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((p, index) => (
                        <tr key={index}>
                            <td>{p.persona}</td>
                            <td>
                                {p.expedientes.join(", ") || "Sin expedientes"}
                            </td>
                            <td>{p.total}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}