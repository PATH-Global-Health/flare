import * as actionTypes from "./actionTypes";
import axios from "../../helpers/axiosFlare";
import { logout } from "./securityActions";

export const fetchResultsSuccess = (results, count) => {
  return {
    type: actionTypes.FETCH_RESULTS_SUCCESS,
    data: results,
    count: count,
  };
};

export const fetchResultsFail = (error) => {
  return {
    type: actionTypes.FETCH_RESULTS_FAIL,
    error: error,
  };
};

export const fetchResultsStart = () => {
  return {
    type: actionTypes.FETCH_RESULTS_START,
  };
};

export const fetchResults = (id, limit, offset, searchTerm) => {
  return (dispatch) => {
    dispatch(fetchResultsStart());

    axios
      .get(
        `/results/?survey_id=${id}&limit=${limit}&offset=${offset}&search=${searchTerm}`
      )
      .then((res) => {
        const results = [];
        const count = res.data.count;

        res.data.results.forEach((result, index) =>
          results.push({ ...result })
        );

        dispatch(fetchResultsSuccess(results, count));
      })
      .catch((err) => {
        if (err.response === undefined) {
          dispatch(fetchResultsFail(err.message));
        } else {
          if (err.response.status === 401 || err.response.status === 403) {
            dispatch(logout());
          } else {
            dispatch(fetchResultsFail(err.response.data.message));
          }
        }
      });
  };
};

export const deleteResultSuccess = () => {
  return {
    type: actionTypes.DELETE_RESULT_SUCCESS,
  };
};

export const removeResultFromList = (resultId) => {
  return {
    type: actionTypes.REMOVE_RESULT,
    resultId: resultId,
  };
};

export const resetDeleteResultSuccess = () => {
  return {
    type: actionTypes.RESET_DELETE_RESULT_SUCCESS,
  };
};

export const deleteResult = (resultId) => {
  return (dispatch) => {
    axios
      .delete(`/results/${resultId}/`)
      .then((res) => {
        dispatch(deleteResultSuccess());
        dispatch(removeResultFromList(resultId));
      })
      .catch((err) => {
        if (err.response === undefined) {
          dispatch(fetchResultsFail(err.message));
        } else {
          dispatch(fetchResultsFail(err.response.data.message));
        }
      });
  };
};
