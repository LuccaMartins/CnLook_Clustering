import numpy as np
import pandas as pd

import scipy.interpolate
import scipy.stats
import scipy.signal

import sklearn.decomposition
from sklearn.base import BaseEstimator, TransformerMixin

import psycopg2

import ast


def connect_db(host, dbname):
    return psycopg2.connect(user='postgres', password='2022', host='localhost', database=dbname)

    #return psycopg2.connect(dbname=dbname, user="postgres", password="2021", host=host)


def read_entity(conn, entity):
    """Read entire table from the database.

    Returns a pandas dataframe. For example, to read the table `subject_entity`,
    use `read_entity(conn, "subject")`.

    """
    index = "%s_id" % entity if entity != "task" else "id"
    df = pd.read_sql_query("SELECT * FROM %s;",
                           conn,
                           params=["%s_entity" % entity],
                           index_col=index)
    assert df.shape != (0, 0), "Table appears to be empty"
    return df


def get_subject_names_for_recordings(conn):
    """Get subject names for all recording ids.

    Returns a dict mapping recording ids to subject names as str.

    """
    cur = conn.cursor()
    cur.execute("""
    SELECT r.recording_id, s.name
    FROM recording_entity AS r
      JOIN screening_entity USING (screening_id)
      JOIN subject_entity AS s USING (subject_id);
    """)
    res = {rec: name for rec, name in cur.fetchall()}
    cur.close()
    return res


def get_all_tasks(conn, group=None):
    """Read all distinct task names from the database.

    If a group is provided, return only tasks that have been performed by at
    least one participant from the group.

    """
    cur = conn.cursor()
    if group is None:
        cur.execute(
            "SELECT DISTINCT name FROM recording_entity ORDER BY name;")
    else:
        cur.execute(
            """
        SELECT DISTINCT r.name
        FROM recording_entity AS r
          JOIN screening_entity USING (screening_id)
          JOIN subject_entity AS s USING (subject_id)
          JOIN group_entity AS g ON (s.group_id = g.id)
        WHERE g.name = %s
        ORDER BY name;
        """, (group, ))
    res = [r[0] for r in cur.fetchall()]  # flatten result
    cur.close()
    return res

def get_sample_recording(conn, recording_id):
    """Read data of a specific sample (task)"""
    cur = conn.cursor()
    cur.execute("SELECT recording_id, timestamp, left_pupil_diameter_mm, right_pupil_diameter_mm FROM sample_entity WHERE recording_id=%(id)s", {'id': recording_id})
    res = cur.fetchall()  # flatten result
    #res = [r[0] for r in cur.fetchall()]  # flatten result
    cur.close()
    return res

def get_specific_recording_by_id(conn, recording_id):
    """Read data of a specific recording"""
    cur = conn.cursor()
    cur.execute("SELECT * FROM recording_entity WHERE recording_id=%(id)s", {'id': recording_id})
    res = cur.fetchall()  # flatten result
    #res = [r[0] for r in cur.fetchall()]  # flatten result
    cur.close()
    return res

def get_specific_recording(conn, screening_id):
    """Read data of a specific recording"""
    cur = conn.cursor()
    cur.execute("SELECT * FROM recording_entity WHERE screening_id=%(id)s", {'id': screening_id})
    res = cur.fetchall()  # flatten result
    #res = [r[0] for r in cur.fetchall()]  # flatten result
    cur.close()
    return res


def get_specific_group_entities(conn, group_id):
    """Read data of a specific group"""
    cur = conn.cursor()
    cur.execute("SELECT * FROM subject_entity WHERE group_id=%(id)s", {'id': group_id})
    res = cur.fetchall()  # flatten result
    #res = [r[0] for r in cur.fetchall()]  # flatten result
    cur.close()
    return res


def get_specific_subject_entities(conn, subject_id):
    """Read data of specific entity"""
    cur = conn.cursor()
    cur.execute("SELECT * FROM screening_entity WHERE subject_id=%(id)s", {'id': subject_id})
    res = cur.fetchall()  # flatten result
    #res = [r[0] for r in cur.fetchall()]  # flatten result
    cur.close()
    return res


def get_all_groups(conn):
    """Read all distinct subject group names from the database."""
    cur = conn.cursor()
    #cur.execute("SELECT DISTINCT name FROM group_entity ORDER BY name;")
    cur.execute("SELECT * FROM group_entity ORDER BY id;")
    res = cur.fetchall()  # flatten result
    #res = [r[0] for r in cur.fetchall()]  # flatten result
    cur.close()
    return res


def read_task_data(conn, group, taskname):
    """Read the data from the database.

    Returns a pandas dataframe indexed by recording_id with columns `timestamp`,
    `left_x`, `left_y`, `right_x`, `right_y`.
    """
    df = pd.read_sql_query(  #
        """
        SELECT
          recording_id, timestamp, left_normal, right_normal, left_pupil_diameter_mm, right_pupil_diameter_mm
        FROM sample_entity AS sample
          JOIN recording_entity AS rec USING (recording_id)
          JOIN screening_entity AS scr USING (screening_id)
          JOIN subject_entity AS subj USING (subject_id)
          JOIN group_entity AS grp ON (grp.id = subj.group_id)
        WHERE rec.name = %s AND grp.name = %s
        ORDER BY recording_id, timestamp;
        """,
        conn,
        index_col="recording_id",
        params=[taskname, group])
    assert df.shape[0] != 0, \
        "no recordings found in database for task %s" % taskname
    for eye in 'left', 'right':
        col = '%s_normal' % eye
        eye_data = np.array([[*ast.literal_eval(t)] for t in df[col]])
        if eye_data.ndim == 1:
            print(eye_data)
            print(df, df.shape)
        df = df.assign(**{
            '%s_x' % eye: eye_data[:, 0],
            '%s_y' % eye: eye_data[:, 1],
        })
    del df['left_normal']
    del df['right_normal']
    df.attrs['taskname'] = taskname
    df.attrs['groupname'] = group
    df.attrs['dbname'] = conn.get_dsn_parameters()['dbname']
    return df

def getRecordings_ByTaskId(conn, taskId, groupId=-1):
    """Read the data from the database.

    Returns a pandas dataframe indexed by recording_id with columns `timestamp`,
    `left_x`, `left_y`, `right_x`, `right_y`, `left_pupil_diameter_mm`, `right_pupil_diameter_mm`.
    """
    if groupId != -1:
        df = pd.read_sql_query(  #
            """
            SELECT
              recording_id, timestamp, tracking_status, left_normal, right_normal, left_pupil_diameter_mm, right_pupil_diameter_mm
            FROM sample_entity AS sample
              JOIN recording_entity AS rec USING (recording_id)
              JOIN screening_entity AS scr USING (screening_id)
              JOIN subject_entity AS subj USING (subject_id)
              JOIN group_entity AS grp ON (grp.id = subj.group_id)
            WHERE rec.task_id = %s AND grp.id = %s
            ORDER BY recording_id, timestamp 
            ;
            """,
            conn,
            index_col="recording_id",
            params=[taskId, groupId])
    else:
        df = pd.read_sql_query(  #
            """
            SELECT
              recording_id, timestamp, tracking_status, left_normal, right_normal, left_pupil_diameter_mm, right_pupil_diameter_mm
            FROM sample_entity AS sample
              JOIN recording_entity AS rec USING (recording_id)
              JOIN screening_entity AS scr USING (screening_id)
              JOIN subject_entity AS subj USING (subject_id)
              JOIN group_entity AS grp ON (grp.id = subj.group_id)
            WHERE rec.task_id = %s
            ORDER BY recording_id, timestamp 
            ;
            """,
            conn,
            index_col="recording_id",
            params=[taskId])

    assert df.shape[0] != 0, \
        "no recordings found in database for task %s" % taskId
    for eye in 'left', 'right':
        col = '%s_normal' % eye
        eye_data = np.array([[*ast.literal_eval(t)] for t in df[col]])
        if eye_data.ndim == 1:
            print(eye_data)
            print(df, df.shape)
        df = df.assign(**{
            '%s_x' % eye: eye_data[:, 0],
            '%s_y' % eye: eye_data[:, 1],
        })
    del df['left_normal']
    del df['right_normal']
    df.attrs['taskId'] = taskId
    df.attrs['groupId'] = groupId
    df.attrs['dbname'] = conn.get_dsn_parameters()['dbname']
    return df.groupby(['recording_id'])

def getTask_ByRecordingId(conn, recId):
    """Read the data from the database.

    Returns a pandas dataframe indexed by recording_id with columns `id`,
    `animation_blueprint`, `parameter_type`, `parameter_data`mm`.
    """
    df = pd.read_sql_query(  #
        """
        select tsk.id, tsk.animation_blueprint, tsk.parameter_type, tsk.parameter_data from task_entity tsk 
        join recording_entity rec on tsk.id = rec.task_id
        where rec.recording_id = %s
        """,
        conn,
        index_col="id",
        params=[recId])
    assert df.shape[0] != 0, \
        "no recordings found in database for id %s" % recId

    df.attrs['dbname'] = conn.get_dsn_parameters()['dbname']

    return df

def getTask_ById(conn, task_id):
    """Read the data from the database.

    Returns a pandas dataframe indexed by id with columns `id`,
    `animation_blueprint`, `parameter_type`, `parameter_data`mm`.
    """
    df = pd.read_sql_query(  #
        """
        select * from task_entity tsk 
        where tsk.id = %s
        """,
        conn,
        index_col="id",
        params=[task_id])
    assert df.shape[0] != 0, \
        "no tasks found in database for id %s" % task_id

    df.attrs['dbname'] = conn.get_dsn_parameters()['dbname']

    return df

class EquidistantResampler(BaseEstimator, TransformerMixin):
    """Resample the ET data to an equidistant time grid.

        This simply performs a linear interpolation of the data and then
        resamples on an equidistant time grid. Rrationale: linear interpolation
        is very fast, and the samples from the ET are almost equidistant at 1ms
        anyway, so this should be accurate enough unless resampling on very fine
        time grids.

    """
    def __init__(self, step):
        """Initialize the equidistant resampler.

        step is the timestep size used to obtain the resampled data.

        """
        if step < 500:
            print(
                "WARNING: You are resampling the data on a very fine time mesh. The quality of the result will suffer. A timestep of 1000 (1ms) is recommended."
            )

        self.step = step

    def fit(self, df):
        """Fit the transformer to the data.

        In this case, no-op.

        """
        return self

    def transform(self, df):
        """Resample ET data."""
        def series_num_samples(series):
            times = series[0]
            duration = times[-1] - times[0]
            return int(duration // self.step)

        total_num_samples = sum(
            map(lambda rec: series_num_samples(df.loc[rec].to_numpy().T),
                df.index.unique()))
        res_data = np.empty((total_num_samples, 5), dtype=float)
        res_index = np.empty(total_num_samples, dtype=int)

        cur_row = 0
        for rec in df.index.unique():
            times = df.loc[rec, 'timestamp'].to_numpy()
            data = df.loc[rec, df.columns != 'timestamp'].to_numpy().T
            interp = scipy.interpolate.interp1d(times,
                                                data,
                                                kind='linear',
                                                copy=False)
            duration = times[-1] - times[0]
            num_samples = int(duration // self.step)
            new_times = np.linspace(times[0],
                                    times[0] + (num_samples - 1) * self.step,
                                    num_samples)
            resampled = np.vstack([new_times, interp(new_times)]).T
            n_rows = resampled.shape[0]
            res_data[cur_row:cur_row + n_rows] = resampled
            res_index[cur_row:cur_row + n_rows] = np.full(n_rows,
                                                          rec,
                                                          dtype=int)
            cur_row += n_rows

        df_resampled = pd.DataFrame(data=res_data,
                                    index=res_index,
                                    columns=df.columns)
        for k, v in df.attrs.items():
            df_resampled.attrs[k] = v
        # store metadata about this operation
        df_resampled.attrs['equi_time_step'] = self.step
        return df_resampled


class GaussianSmoother(BaseEstimator, TransformerMixin):
    """Smooth the ET data.

    Convolves the time series with a gaussian kernel of the given standard
    deviation to apply smoothing. The data must have previously been resampled
    to equidistant timestamps!

    """
    def __init__(self, sigma):
        """Initialize the gaussian smoother.

        sigma is the standard deviation used for the gaussian kernel in the
        smoothing convolution (see `transform`).

        """
        self.sigma = sigma

    def fit(self, df):
        """Fit the transformer to the data.

        In this case, no-op.

        """
        return self

    def transform(self, df):
        """Smooth the ET data."""
        assert 'equi_time_step' in df.attrs, \
            "The data must have been resampled to equidistant timestamps to apply the smoothing convolution."

        step = df.attrs['equi_time_step']
        kernel_size = 1 + 2 * int(3 * self.sigma // step)
        kernel = scipy.stats.norm(0.0, self.sigma).pdf(
            np.linspace(-3 * self.sigma, 3 * self.sigma, kernel_size))
        kernel /= np.linalg.norm(kernel,
                                 ord=1)  # compensate discrete sampling of pdf
        df_smoothed = df.copy()
        for rec in df.index.unique():
            data = df.loc[rec, df.columns != 'timestamp'].to_numpy().T
            data = np.pad(data, [(0, 0), (kernel_size // 2, kernel_size // 2)],
                          mode='reflect')
            for idx, feature in enumerate(
                    df.columns[df.columns != 'timestamp']):
                smoothed = scipy.signal.convolve(data[idx],
                                                 kernel,
                                                 mode='valid')
                df_smoothed.loc[rec, feature] = smoothed
        return df_smoothed


class ETNormalizer(BaseEstimator, TransformerMixin):
    """Centre the time series data around its mean.

    The data must have been resampled to an equal and equidistant time grid.

    """
    def __init__(self):
        pass

    def fit(self, df):
        """Fit the transformer to the data.

        In this case, computes the time series mean of the given training data.

        """
        assert 'equi_time_step' in df.attrs, \
            "The data must have been resampled to an equidistant and equal time grid for this operation to make sense."
        data = [
            df.loc[rec, df.columns != 'timestamp'].to_numpy()
            for rec in df.index.unique()
        ]
        self.max_rows = max(map(lambda d: d.shape[0], data))
        data = [
            np.pad(d, [(0, self.max_rows - d.shape[0]), (0, 0)],
                   mode='constant',
                   constant_values=np.nan) for d in data
        ]
        self.mean = np.nanmean(np.stack(data), axis=0)
        return self

    def transform(self, df):
        """Centre the data around the training mean."""
        df2 = df.copy()
        for rec in df.index.unique():
            n = min(df2.loc[rec].shape[0], self.max_rows)
            df2.loc[rec, df2.columns != 'timestamp'][:n] -= self.mean[:n]
        return df2


class DropShortSequences(BaseEstimator, TransformerMixin):
    """Drop short samples."""
    def __init__(self, threshold_time):
        self.threshold_time = threshold_time

    def fit(self, df):
        """Fit the transformer to the data.

        In this case, no-op.

        """
        return self

    def transform(self, df):
        """Drop sequences shorter than `self.threshold_time`."""
        def is_long_enough(series):
            duration = float(series['timestamp'].tail(1) -
                             series['timestamp'].head(1))
            return duration >= self.threshold_time

        okay_recs = {
            rec
            for rec in df.index.unique() if is_long_enough(df.loc[rec])
        }
        return df.loc[okay_recs]


class ScoreTransformer(BaseEstimator, TransformerMixin):
    """Helper class to convert estimators to transformers.

    Paramters
    ---------
    scorer : object
        Any object that possesses both a `fit(self, df)` and a
        `score_samples(self, df)` method.
    """
    def __init__(self, scorer):
        self.scorer = scorer

    def fit(self, df, y, *args):
        assert y is None and len(args) == 0, "Does not support passing arguments."
        self.scorer.fit(df)

    def transform(self, df):
        return self.scorer.score_samples(df)


class JoinFrames(BaseEstimator, TransformerMixin):
    """Helper class that joins dataframes resulting from child transformers.

    Parameters
    ----------
    steps : list of tuple
        List of (name, transform) tuples (implementing `fit`/`transform`). These
        transformers will be run "in parallel" and their resulting dataframes
        will be joined.
    """
    def __init__(self, steps):
        self.steps = steps

    def fit(self, df):
        for _, step in self.steps:
            step.fit(df)

    def transform(self, df):
        if len(self.steps) == 0:
            return None
        transformed = [step.transform(df) for _, step in self.steps]
        if len(self.steps) == 1:
            return transformed[0]

        return transformed[0].join(transformed[1:], how='inner')


class ConvPCA(sklearn.decomposition.PCA):
    """Hacky 'convolutional' PCA on time series data.

    Parameters
    ----------
    filter_length : int
        The length (in microseconds) of the PCA filter.

    stride_time : int
        The time (in microseconds) by which filter applications are offset.

    n_components : int
        The number of PCA components, see also `sklearn.decomposition.PCA`.
    """
    def __init__(self,
                 filter_length,
                 stride_time,
                 n_components):
        self._super = super(ConvPCA, self)
        self._super.__init__(n_components)

        self.filter_length = filter_length
        self.stride_time = stride_time

    def _conv_windows_of(self, rec_data):
        num_samples = rec_data.shape[1]
        assert num_samples >= self.filter_size, "filter size is too large for data"
        n_windows = 1 + (num_samples - self.filter_size) // self.stride

        as_strided = np.lib.stride_tricks.as_strided
        windows = []
        for row in rec_data[1:]:  # left and right eye, x and y
            data_stride = row.strides[0]
            windows.append(
                as_strided(row, (n_windows, self.filter_size),
                           (self.stride * data_stride, data_stride)))
        return np.hstack(windows)

    def fit(self, df):
        assert 'equi_time_step' in df.attrs, \
            "The data must have been resampled to an equidistant and equal time grid for this operation to make sense."
        self.step = df.attrs['equi_time_step']
        self.filter_size = int(self.filter_length // self.step)
        self.stride = int(self.stride_time // self.step)
        assert self.filter_size > 0, "Filter size must be positive. Try choosing a longer filter length for this data."
        assert self.stride > 0, "Stride time must be at least the step size in the data."

        reshaped = np.vstack([
            self._conv_windows_of(df.loc[rec].to_numpy().T)
            for rec in df.index.unique()
        ])
        self._super.fit(reshaped)
        return self

    def score_samples(self, df, output_series=False):
        """
        Obtain error between data and PCA-projected data.

        Parameters
        ----------
        output_series : bool, default=False
            Whether to output the series of scores in addition to the overall
            score.
        """
        assert 'equi_time_step' in df.attrs, \
            "The data must have been resampled to an equidistant and equal time grid for this operation to make sense."
        assert df.attrs['equi_time_step'] == self.step, \
            "The data must have the same sampling rate as the training data."

        V = self.components_
        scores = pd.DataFrame(columns=['pca_score'])
        for rec, windows in [(rec,
                              self._conv_windows_of(df.loc[rec].to_numpy().T))
                             for rec in df.index.unique()]:
            score_series = np.array(
                [np.linalg.norm(V.T @ (V @ w) - w) for w in windows])
            score = np.linalg.norm(score_series)
            scores.loc[rec] = (score, score_series) if output_series else score
        return scores


class FreqScorer(BaseEstimator):
    """Score series based on amount of high frequency content.

    Parameters
    ----------
    sigma : float
        The standard deviation used for the gaussian high-pass filter to extract
        high frequency content.
    """
    def __init__(self, sigma):
        self.sigma = sigma

    def fit(self, df):
        pass

    def score_samples(self, df, output_series=False):
        """
        Score amout of high-frequency content in data.

        Applies a high-pass gaussian filter and computes the L2 (Frobenius) norm
        of the resulting signal.

        Parameters
        ----------
        output_series : bool, default=False
            Whether to output the high-pass filtered signal along with the score
        """
        assert 'equi_time_step' in df.attrs, \
            "The data must have been resampled to an equidistant and equal time grid for this operation to make sense."
        step = df.attrs['equi_time_step']

        # Step 1: Construct high-pass filter
        kernel_size = 1 + 2 * int(3 * self.sigma // step)
        kernel = scipy.stats.norm(0.0, self.sigma).pdf(
            np.linspace(-3 * self.sigma, 3 * self.sigma, kernel_size))
        kernel = -kernel / np.linalg.norm(kernel, ord=1)
        kernel[kernel_size // 2] += 1.0

        # Step 2: Convolve with filter and score remaining content
        scores = pd.DataFrame(columns=['freq_score'])
        for rec in df.index.unique():
            data = df.loc[rec, df.columns != 'timestamp'].to_numpy().T
            filtered = np.empty(data.shape)
            data = np.pad(data, [(0, 0), (kernel_size // 2, kernel_size // 2)],
                          mode='reflect')
            for idx, row in enumerate(data):
                filtered[idx] = scipy.signal.convolve(row, kernel, mode='valid')
            norm = np.linalg.norm(filtered, ord='fro')  # Frobenius norm
            scores.loc[rec] = (norm, filtered) if output_series else norm
        return scores


class LeftRightCorrScorer(BaseEstimator, TransformerMixin):
    """Score series based on correlation between left and right eye."""
    def __init__(self):
        pass

    def fit(self, df):
        pass

    def score_samples(self, df):
        assert 'equi_time_step' in df.attrs, "The data must have been resampled to an equidistant and equal time grid for this operation to make sense."

        # The un-normalized correlation is just the inner product (we are not
        # interested in any signal delay etc). Since each series (left and right
        # eye) consists of 2D vectors (x and y), one could consider the series
        # as elements of the tensor product space between x and y, in which case
        # the inner product of the two series becomes the sum of the two scalar
        # products (x and y).

        scores = pd.DataFrame(columns=['corr_score'])
        for rec in df.index.unique():
            data = df.loc[rec, df.columns != 'timestamp'].to_numpy().T
            assert data.shape[0] == 4
            corr = np.dot(data[0], data[2]) + np.dot(
                data[1], data[3])
            # normalize
            corr /= sum([np.dot(row, row) for row in data])

            scores.loc[rec] = corr
        return scores
