import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

export const detectPreview = async (file: File, token: string) => {
  const formData = new FormData();
  formData.append("file", file);

  const res = await api.post("/image/detect-preview", formData, {
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "multipart/form-data",
    },
  });

  return res.data;
};

export const segmentPreview = async (file: File, token: string) => {
  const formData = new FormData();
  formData.append("file", file);

  const res = await api.post("/image/segment-preview", formData, {
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "multipart/form-data",
    },
  });

  return res.data;
};
