import { doRequest } from "./client";

export const processRegister = async ({ login, password }) => {
  const response = await doRequest({
    type: "POST",
    uri: "/register",
    body: {
      login: login,
      password: password,
    },
  });
  console.log("Register: response:", response);

  return response;
};
