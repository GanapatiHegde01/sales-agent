import api from "./api";

export const getProducts = async (page = 1, per_page = 20) => {
  const res = await api.get("/products", { params: { page, per_page } });
  return res.data;
};

export const getProduct = async (id) => {
  const res = await api.get(`/products/${id}`);
  return res.data;
};

export const getOffers = async () => {
  const res = await api.get("/offers");
  return res.data;
};

export const getWarranty = async (productId) => {
  const res = await api.get(`/warranty/${productId}`);
  return res.data;
};
