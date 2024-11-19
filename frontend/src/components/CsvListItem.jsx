import React from "react";
import { Link } from "react-router-dom";
import "../styles/CsvListItem.css"

function CsvListItem({ csv, onDelete }) {

    return (
        <div className="csv-container">
            <a href={`/csvs/${csv.id}`} className="csv-file-name">{csv.file_name}</a>
            <button className="delete-button" onClick={() => onDelete(csv.id)}>
                Delete
            </button>
        </div>
    );
}

export default CsvListItem;
