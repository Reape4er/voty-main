import axios from "axios";

export default async function ({ app, redirect, store }) {
  console.log("Middleware is running");
  const token = app.$cookies.get("token");

  if (token) {
    console.log("Token found:", token);

    try {
      const response = await axios.get(
        "http://localhost:8000/check_token",
        {
          headers: {
            Authorization: "Bearer " + token,
          },
        }
      );
      const user = {
        id: response.data.id,
        firstName: response.data.firstName,
        lastName: response.data.lastName,
        middleName: response.data.middleName,
        email: response.data.email,
        role: response.data.role,
      };
      store.commit("SET_USER", user);
      console.log("Token is valid:", response.data);
    } catch (error) {
      console.error("Error checking token:", error);
      redirect("/signin");
    }
  } else {
    store.commit("REMOVE_USER");
    console.log("No token found");
    redirect("/signin");
  }
}
