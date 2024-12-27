import { AuthStatus, onLogOut, setBalance } from "../app/reducers/authData";
import client, { doRequest, RequestType } from "./client";

export const LogInOutProcess = async (authStatus, token = "") => {
  if (authStatus == AuthStatus.logged) {
    return async ({ dispatch, navigate }) => {
      dispatch(onLogOut());
      navigate("/");
      await client.post("/logout");
    };
  } else if (authStatus == AuthStatus.notLogged) {
    return async ({ dispatch, navigate }) => {
      navigate("/auth");
    };
  }

  console.log("LogInOutProcess: error: undefined authStatus: ", authStatus);
  return () => {};
};
