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

export const doRequest = async ({ type, uri, params = {}, body = {} }, token = "") => {
  console.log("doRequest: uri: ", {type, uri, params, body}, "token: ", token);
  const headers = {}
  if(token != "") {
    headers["authorization"] = `Bearer ${token}`;
  }

  switch (type) {
    case RequestType.get:
      return await client.get(uri, { params: params, headers: headers});
    case RequestType.post:
      return await client.post(uri, body, { params: params, headers: headers });
    case RequestType.put:
      return await client.put(uri, body, { params: params, headers: headers });
    case RequestType.delete:
      return await client.delete(uri, { params: params, headers: headers });
  }
};

export default client;
