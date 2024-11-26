import axios from "axios";

const API_BASE_URL = "https://laughing-engine-x9vpgpv4pppcpjrr-8000.app.github.dev";

// Utility function to handle axios requests
const axiosRequest = async (method, url, data = null, headers = {}) => {
  try {
    const response = await axios({
      method,
      url: `${API_BASE_URL}${url}`,
      data,
      headers,
    });
    return response.data;
  } catch (error) {
    console.error(`Error with ${url}:`, error);
    throw new Error(`Failed to fetch from ${url}`);
  }
};

export const evaluateDeal = (dealData) =>
  axiosRequest("post", "/evaluate-deal", dealData);

export const uploadCSV = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return axiosRequest("post", "/upload-csv", formData, {
    "Content-Type": "multipart/form-data",
  });
};

export const updateConfig = (config) =>
  axiosRequest("put", "/update-config", config);

export const updateIndustryMultiples = (multiples) =>
  axiosRequest("put", "/update-industry-multiples", multiples);

export const getConfig = () => axiosRequest("get", "/get-config");

export const getIndustryMultiples = () =>
  axiosRequest("get", "/get-industry-multiples");
