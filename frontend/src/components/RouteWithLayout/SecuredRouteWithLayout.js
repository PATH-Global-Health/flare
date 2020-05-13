import React from "react";
import { Route } from "react-router-dom";
import PropTypes from "prop-types";
import { useSelector } from "react-redux";
import { Redirect } from "react-router-dom";

const SecuredRouteWithLayout = (props) => {
  const { layout: Layout, component: Component, ...rest } = props;
  const { isAuthenticated } = useSelector((state) => ({
    isAuthenticated: state.security.isAuthenticated,
  }));

  return (
    <Route
      {...rest}
      render={(matchProps) => (
        <Layout>
          {isAuthenticated ? (
            <Component {...matchProps} />
          ) : (
            <Redirect to="/sign-in" />
          )}
        </Layout>
      )}
    />
  );
};

SecuredRouteWithLayout.propTypes = {
  component: PropTypes.any.isRequired,
  layout: PropTypes.any.isRequired,
  path: PropTypes.string,
};

export default SecuredRouteWithLayout;
