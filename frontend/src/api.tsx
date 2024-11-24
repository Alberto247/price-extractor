import axios, { AxiosError } from "axios";

const API_BASE_URL = ""; // Replace with your backend URL

type Offer = {
    type: "offer";
    name: string;
    currency: string;
    price: number;
};

type MultipleOffers = {
    type: "multipleOffers";
    name: string;
    currency: string;
    tot_offers: number;
    min_price: number;
    max_price: number;
};

export type DataItem = Offer | MultipleOffers;

interface ApiResponse {
    success: boolean;
    data?: DataItem[];
    error?: string;
}

export const extractData = async (url: string): Promise<ApiResponse> => {
    try {
        const response = await axios.get<ApiResponse>(`${API_BASE_URL}/extract/${encodeURIComponent(url)}`);
        return response.data;
    } catch (err) {
        // Explicitly type the error as AxiosError
        const error = err as AxiosError<ApiResponse>;

        return {
            success: false,
            error: error.response?.data?.error || "An unknown error occurred.",
        };
    }
};