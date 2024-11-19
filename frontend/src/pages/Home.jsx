import { useState, useEffect } from "react";
import api from "../api";
import CsvListItem from "../components/CsvListItem"
import "../styles/Home.css"

function Home() {
    const [csvs, setCsvs] = useState([]);
    const [csv_file, setSelectedFile] = useState(null);

    useEffect(() => {
        getCsvs();
    }, []);

    const handleFileChange = (e) => { 
        setSelectedFile(e.target.files[0]); 
    };

    const getCsvs = () => {
        api
            .get("/api/csvs/")
            .then((res) => res.data)
            .then((data) => {
                setCsvs(data);
                console.log(data);
            })
            .catch((err) => alert(err));
    };

    const deleteCsv = (id) => {
        api
            .delete(`/api/csvs/${id}/`)
            .then((res) => {
                if (res.status === 204) alert("Csv deleted!");
                else alert("Failed to delete csv.");
                getCsvs();
            })
            .catch((error) => alert(error));
    };

    const createCsv = (e) => {
        e.preventDefault();
        api
            .post("/api/csvs/", { csv_file })
            .then((res) => {
                if (res.status === 201) alert("Csv created!");
                else alert("Failed to make csv.");
                getCsvs();
            })
            .catch((err) => alert(err));
    };

    return (
        <div>
            <div>
                <h2>Csvs</h2>
                {csvs.map((csv) => (
                    <CsvListItem csv={csv} onDelete={deleteCsv} key={csv.id} />
                ))}
            </div>
            <h2>Create a Csv</h2>
            <form onSubmit={createCsv}>
                <label htmlFor="csv_file">Csv File:</label>
                <br />
                <input
                    type="file"
                    accept=".csv, application/vnd.ms-excel, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    onChange={handleFileChange}
                    required
                />
                <br />
                <input type="submit" value="Submit"></input>
            </form>
        </div>
    );
}

export default Home;