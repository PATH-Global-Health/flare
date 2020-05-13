import React from "react";
import { Switch, Redirect } from "react-router-dom";

import { RouteWithLayout, SecuredRouteWithLayout } from "./components";
import { Main as MainLayout, Minimal as MinimalLayout } from "./layouts";

import {
  Dashboard as DashboardView,
  SignIn as SignInView,
  NotFound as NotFoundView,
  LanguageList as LanguageListView,
  LanguageAdd as LanguageAddView,
  LanguageEdit as LanguageEditView,
  SubscriberList as SubscriberListView,
  SubscriberAdd as SubscriberAddView,
  SubscriberEdit as SubscriberEditView,
  MessageList as MessageListView,
  MessageAdd as MessageAddView,
  SurveyList as SurveyListView,
  SurveyAdd as SurveyAddView,
  SurveyEdit as SurveyEditView,
  ResultList as ResultListView,
} from "./views";

const Routes = () => {
  const routes = (
    <Switch>
      <Redirect exact from="/" to="/dashboard" />
      <SecuredRouteWithLayout
        component={DashboardView}
        exact
        layout={MainLayout}
        path="/dashboard"
      />
      <SecuredRouteWithLayout
        component={LanguageListView}
        exact
        layout={MainLayout}
        path="/language"
      />
      <SecuredRouteWithLayout
        component={LanguageAddView}
        exact
        layout={MainLayout}
        path="/language/add"
      />
      <SecuredRouteWithLayout
        component={LanguageEditView}
        exact
        layout={MainLayout}
        path="/language/edit/:id"
      />
      <SecuredRouteWithLayout
        component={SubscriberListView}
        exact
        layout={MainLayout}
        path="/subscriber"
      />
      <SecuredRouteWithLayout
        component={SubscriberAddView}
        exact
        layout={MainLayout}
        path="/subscriber/add"
      />
      <SecuredRouteWithLayout
        component={SubscriberEditView}
        exact
        layout={MainLayout}
        path="/subscriber/edit/:id"
      />
      <SecuredRouteWithLayout
        component={MessageListView}
        exact
        layout={MainLayout}
        path="/message"
      />
      <SecuredRouteWithLayout
        component={MessageAddView}
        exact
        layout={MainLayout}
        path="/message/add"
      />

      <SecuredRouteWithLayout
        component={SurveyListView}
        exact
        layout={MainLayout}
        path="/survey"
      />
      <SecuredRouteWithLayout
        component={SurveyAddView}
        exact
        layout={MainLayout}
        path="/survey/add"
      />
      <SecuredRouteWithLayout
        component={SurveyEditView}
        exact
        layout={MainLayout}
        path="/survey/edit/:id"
      />

      <SecuredRouteWithLayout
        component={ResultListView}
        exact
        layout={MainLayout}
        path="/result/:id"
      />

      <RouteWithLayout
        component={SignInView}
        exact
        layout={MinimalLayout}
        path="/sign-in"
      />

      <SecuredRouteWithLayout
        component={NotFoundView}
        exact
        layout={MainLayout}
        path="/not-found"
      />
      <Redirect to="/not-found" />
    </Switch>
  );

  return routes;
};

export default Routes;
