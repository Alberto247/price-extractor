import React from "react";
import { DataItem } from "../api";

interface ResultsProps {
    items: DataItem[];
}

const Results: React.FC<ResultsProps> = ({ items }) => {
    return (
        <div style={{ marginTop: "1rem" }}>
            <h2>Extracted Data:</h2>
            <ul style={{ padding: "0", listStyle: "none" }}>
                {items.map((item, index) => (
                    <li
                        key={index}
                        style={{
                            padding: "0.5rem",
                            backgroundColor: "#f9f9f9",
                            marginBottom: "0.5rem",
                            borderRadius: "4px",
                        }}
                    >
                        <strong>{item.name}</strong> ({item.currency})<br />
                        {item.type === "offer" ? (
                            <div>Price: {item.price}</div>
                        ) : (
                            <div>
                                Total Offers: {item.tot_offers}<br />
                                Min Price: {item.min_price}<br />
                                Max Price: {item.max_price}
                            </div>
                        )}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Results;