import { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';
import api from "../api";
import "../styles/Detail.css";
import Header from "../components/Header";



function Detail() {
    const { id } = useParams();
    const [headers, setHeaders] = useState([]);
    const [rows, setRows] = useState([]);
    const [file_name, setTitle] = useState("");

    useEffect(() => {
        getCsv();
    }, {});

    const getCsv = () => {
        api
            .get(`/api/csvs/${id}/`)
            .then((res) => res.data)
            .then((data) => {
                setHeaders(data.headers);
                setRows(data.rows);
                console.log(data);
            })
            .catch((err) => alert(err));
    };



    return (
        <div>
            <div>
                <a href="/" className="back-button">Back</a>
            </div>

            <div>
                <table>
                    <thead>
                        {
                            headers.map((header, index) => ( 
                                <th key={index}>
                                    <div>{header.name}</div>
                                    <Header 
                                        csv_id={id}
                                        header_id={header.id}
                                        header_type={header.type} 
                                    />
                                </th> 
                            ))
                        }
                    </thead>

                    {
                        rows.map((row, row_index) => (
                            <tbody key={row_index}>
                                {
                                    row.content.map((cell, index) => (
                                        <td key={index}>
                                            {cell}
                                        </td>
                                    ))
                                }
                            </tbody>
                        ))
                    }
                </table>
            </div>
            
        </div>
    );
}

export default Detail;