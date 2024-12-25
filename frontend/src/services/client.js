import { data } from "@remix-run/router";
import axios from "axios";
import addresses from "./addresses";

const client = axios.create({ baseURL: addresses.backend, withCredentials: true });

export const RequestType = {
  get: "GET",
  post: "POST",
  put: "PUT",
  delete: "DELETE",
};

export const doRequest = async ({ type, uri, params = {}, body = {} }) => {
  console.log("doRequest: uri: ", uri);
  switch (type) {
    case RequestType.get:
      return await client.get(uri, { params: params });
    case RequestType.post:
      return await client.post(uri, body, { params: params });
    case RequestType.put:
      return await client.put(uri, body, { params: params });
    case RequestType.delete:
      return await client.delete(uri, { params: params });
  }
};

export default client;
