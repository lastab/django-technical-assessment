import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import { TYPE_OPTIONS } from "../constants";
import Select from 'react-select';

function Header({ csv_id, header_id, header_type }) {


    const updateHeader = (csv_id, header_id, option) => {
        console.log(option)
        api
            .put(`/api/csvs/${csv_id}/headers/${header_id}/`, 
                { type: option.value })
            .then((res) => {
                if (res.status === 200) alert("Type updated!");
                else alert("Failed to update header.");
            })
            .catch((err) => alert(err));
    };

    return (
        <Select 
            onChange={(e) => {updateHeader(csv_id, header_id, e)}}
            
            defaultValue={{
                label: header_type.toUpperCase(),
                value: header_type
            }}
            options={TYPE_OPTIONS}
        />
    );
}

export default Header