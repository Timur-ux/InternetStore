import { AuthStatus, onLogOut, setBalance } from "../app/reducers/authData";
import client, { doRequest, RequestType } from "./client";

export const LogInOutProcess = async (authStatus) => {
  if (authStatus == AuthStatus.logged) {
    return async ({ dispatch, navigate }) => {
      dispatch(onLogOut());
      navigate("/");
      await client.post("/logout");
    };
  } else if (authStatus == AuthStatus.notLogged) {
    return async ({ dispatch, navigate }) => {
      navigate("/auth");
      doRequest({ type: RequestType.get, uri: "/user/balance" })
        .then((response) => {
          dispatch(setBalance(response.data));
        })
        .catch((reason) => {
          dispatch(setBalance(-1));
          console.log("Log in process: error: ", reason);
        });
    };
  }

  console.log("LogInOutProcess: error: undefined authStatus: ", authStatus);
  return () => {};
};
