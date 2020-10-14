import {
  ApolloClient,
  InMemoryCache,
  NormalizedCacheObject,
  ApolloProvider,
} from "@apollo/client";
import React from "react";
import ReactDOM from "react-dom";
import Cookies from "js-cookie";

import Pages from "./pages";
import injectStyles from "./styles";

const client: ApolloClient<NormalizedCacheObject> = new ApolloClient({
  uri: "http://localhost:8000/graphql/",
  cache: new InMemoryCache(),
  headers: {
    "X-CSRFToken": Cookies.get("csrftoken")!,
  },
  credentials: "include",
});

injectStyles();
ReactDOM.render(
  <ApolloProvider client={client}>
    <Pages />
  </ApolloProvider>,
  document.getElementById("root")
);
