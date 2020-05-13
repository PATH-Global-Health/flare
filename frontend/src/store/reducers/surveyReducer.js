import * as actionTypes from "../actions/actionTypes";

const initialState = {
  data: [],
  count: 0,
  loadingSurveys: false,
  saveSuccess: false,
  error: null,
  survey: null,
  loadingSurvey: false,
};

const fetchSurveysStart = (state) => {
  return {
    ...state,
    error: null,
    loadingSurveys: true,
  };
};

const fetchSurveysSuccess = (state, action) => {
  return {
    ...state,
    data: action.data,
    loadingSurveys: false,
    error: null,
    count: action.count,
  };
};

const fetchSurveysFail = (state, action) => {
  return {
    ...state,
    loadingSurveys: false,
    error: action.error,
  };
};

const saveSurveySuccess = (state) => {
  return {
    ...state,
    saveSuccess: true,
  };
};

const resetSaveSurveySuccess = (state, action) => {
  return {
    ...state,
    saveSuccess: false,
  };
};

const fetchSurveyStart = (state) => {
  return {
    ...state,
    error: null,
    loadingSurvey: true,
  };
};

const fetchSurveySuccess = (state, action) => {
  return {
    ...state,
    survey: action.survey,
    loadingSurvey: false,
  };
};

const removeSurveyFromList = (state, action) => {
  return {
    ...state,
    data: state.data.filter((el) => el.id !== action.surveyId),
  };
};

const updateSurveyFail = (state, action) => {
  return {
    ...state,
    error: action.error,
  };
};

const reducer = (state = initialState, action) => {
  switch (action.type) {
    case actionTypes.FETCH_SURVEYS_START:
      return fetchSurveysStart(state);
    case actionTypes.FETCH_SURVEYS_SUCCESS:
      return fetchSurveysSuccess(state, action);
    case actionTypes.FETCH_SURVEYS_FAIL:
      return fetchSurveysFail(state, action);
    case actionTypes.SAVE_SURVEY_SUCCESS:
      return saveSurveySuccess(state);
    case actionTypes.RESET_SAVE_SURVEY_SUCCESS:
      return resetSaveSurveySuccess(state);
    case actionTypes.FETCH_SURVEY_START:
      return fetchSurveyStart(state);
    case actionTypes.FETCH_SURVEY_SUCCESS:
      return fetchSurveySuccess(state, action);
    case actionTypes.REMOVE_SURVEY:
      return removeSurveyFromList(state, action);
    case actionTypes.UPDATE_SURVEY_FAIL:
      return updateSurveyFail(state, action);
    default:
      return state;
  }
};

export default reducer;
