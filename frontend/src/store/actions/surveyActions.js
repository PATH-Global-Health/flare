import * as actionTypes from "./actionTypes";
import axios from "../../helpers/axiosFlare";
import mapResponseErrors from "../../helpers/mapResponseErrors";
import { logout } from "./securityActions";

export const fetchSurveysSuccess = (surveys, count) => {
  return {
    type: actionTypes.FETCH_SURVEYS_SUCCESS,
    data: surveys,
    count: count,
  };
};

export const fetchSurveysFail = (error) => {
  return {
    type: actionTypes.FETCH_SURVEYS_FAIL,
    error: error,
  };
};

export const fetchSurveysStart = () => {
  return {
    type: actionTypes.FETCH_SURVEYS_START,
  };
};

export const fetchSurveys = (limit, offset, searchTerm) => {
  return (dispatch) => {
    dispatch(fetchSurveysStart());

    axios
      .get(`/surveys/?limit=${limit}&offset=${offset}&search=${searchTerm}`)
      .then((res) => {
        const surveys = [];
        const count = res.data.count;

        res.data.results.forEach((survey, index) =>
          surveys.push({ ...survey })
        );

        dispatch(fetchSurveysSuccess(surveys, count));
      })
      .catch((err) => {
        if (err.response === undefined) {
          dispatch(fetchSurveysFail(err.message));
        } else {
          if (err.response.status === 401 || err.response.status === 403) {
            dispatch(logout());
          } else {
            dispatch(fetchSurveysFail(err.response.data.message));
          }
        }
      });
  };
};

export const saveDelSurveySuccess = () => {
  return {
    type: actionTypes.SAVE_SURVEY_SUCCESS,
  };
};

export const resetSaveSurveySuccess = () => {
  return {
    type: actionTypes.RESET_SAVE_SURVEY_SUCCESS,
  };
};

export const updateSurveyFail = (error) => {
  return {
    type: actionTypes.UPDATE_SURVEY_FAIL,
    error: error,
  };
};

export const addSurvey = (survey, history, errorCallback) => {
  return (dispatch) => {
    axios
      .post("/surveys/", survey)

      .then((res) => {
        dispatch(saveDelSurveySuccess());
        history.push("/survey");
      })
      .catch((err) => {
        if (err.response === undefined) {
          dispatch(updateSurveyFail(err.message));
          errorCallback(err.message);
        } else {
          const errors = mapResponseErrors(err.response.data);
          errorCallback(errors);
        }
      });
  };
};

export const fetchSurveySuccess = (survey) => {
  return {
    type: actionTypes.FETCH_SURVEY_SUCCESS,
    survey: survey,
  };
};

export const fetchSurveyStart = () => {
  return {
    type: actionTypes.FETCH_SURVEY_START,
  };
};

export const fetchSurvey = (surveyId, history) => {
  return (dispatch) => {
    dispatch(fetchSurveyStart());

    axios
      .get(`/surveys/${surveyId}`)
      .then((res) => {
        const survey = {
          title: res.data.title,
          published: res.data.published,
          journeys: res.data.journeys,
        };

        dispatch(fetchSurveySuccess(survey));
      })
      .catch((err) => {
        if (err.response === undefined) {
          dispatch(fetchSurveysFail(err.message));
        } else {
          dispatch(fetchSurveysFail(err.response.data.message));
        }
        history.push("/survey/");
      });
  };
};

export const editSurvey = (survey, surveyId, history, errorCallback) => {
  return (dispatch) => {
    axios
      .put(`/surveys/${surveyId}/`, survey)
      .then((res) => {
        dispatch(saveDelSurveySuccess());
        history.push("/survey");
      })
      .catch((err) => {
        console.log(err.response);
        if (err.response === undefined) {
          dispatch(updateSurveyFail(err.message));
          errorCallback(err.message);
        } else {
          const errors = mapResponseErrors(err.response.data);
          errorCallback(errors);
        }
      });
  };
};

export const removeSurveyFromList = (surveyId) => {
  return {
    type: actionTypes.REMOVE_SURVEY,
    surveyId: surveyId,
  };
};

export const deleteSurvey = (surveyId, history) => {
  return (dispatch) => {
    axios
      .delete(`/surveys/${surveyId}/`)
      .then((res) => {
        dispatch(saveDelSurveySuccess());
        dispatch(removeSurveyFromList(surveyId));
      })
      .catch((err) => {
        if (err.response === undefined) {
          dispatch(fetchSurveysFail(err.message));
        } else {
          dispatch(fetchSurveysFail(err.response.data.message));
        }
      });
  };
};
