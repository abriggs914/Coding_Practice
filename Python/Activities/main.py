import datetime as dt
from typing import Iterable

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from streamlit_utility import display_df


st.set_page_config(layout="wide", page_title="Activities", page_icon=":biking_man:")

PATH_EXCEL_DATA = "data.xlsx"
ROLLING_WINDOWS = [2, 3, 5, 7, 14, 21, 31, 62, 90, 180]
CORE_AGGS = ["sum", "mean", "median", "min", "max", "count", "std", "var", "sem", "nunique", "skew"]


# -----------------------------
# Loading and preparation
# -----------------------------
@st.cache_data(show_spinner="Loading activity data...")
def load_data(path: str = PATH_EXCEL_DATA, seconds_as_hours="s") -> pd.DataFrame:
    df = pd.read_excel(path)
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]

    if "date" not in df.columns:
        raise ValueError("Expected a 'date' column in data.xlsx")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"]).sort_values("date")

    if "activity" not in df.columns:
        df["activity"] = "Activity"
    if "unit" not in df.columns:
        df["unit"] = ""
        
    if seconds_as_hours != "s":
        for i, r in df.iterrows():
            df.loc[i, ["times", "unit"]] = (r["times"], r["unit"]) if r["unit"] != "sec" else (
                (r["times"] / 86400, "min") if seconds_as_hours == "d" else (
                    (r["times"] / 60, "min") if seconds_as_hours == "m" else (r["times"] / 3600, "hrs")
                )
            )

    # Keep dates as timestamps for rolling calculations and Plotly.
    return df.reset_index(drop=True)


def get_numeric_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in df.select_dtypes(include="number").columns if not c.lower().endswith("id")]


def safe_mode(series: pd.Series):
    s = series.dropna()
    if s.empty:
        return np.nan
    m = s.mode()
    return m.iloc[0] if not m.empty else np.nan


def fmt_value(value, digits: int = 2) -> str:
    if pd.isna(value):
        return "—"
    if isinstance(value, (pd.Timestamp, dt.date, dt.datetime)):
        return pd.to_datetime(value).strftime("%Y-%m-%d")
    if isinstance(value, (np.integer, int)):
        return f"{int(value):,}"
    if isinstance(value, (np.floating, float)):
        return f"{value:,.{digits}f}"
    return str(value)


# -----------------------------
# Summary tables
# -----------------------------
def build_activity_summary(df: pd.DataFrame, numeric_cols: Iterable[str]) -> pd.DataFrame:
    work = df.copy()
    agg_map = {col: CORE_AGGS for col in numeric_cols}
    summary = work.groupby(["activity", "unit"], dropna=False).agg(agg_map)
    summary.columns = [f"{agg}_{col}" for col, agg in summary.columns]
    summary = summary.reset_index()

    date_summary = work.groupby(["activity", "unit"], dropna=False).agg(
        first_date=("date", "min"),
        last_date=("date", "max"),
        active_days=("date", lambda s: s.dt.normalize().nunique()),
        records=("date", "size"),
    ).reset_index()

    summary = date_summary.merge(summary, on=["activity", "unit"], how="left")
    summary["date_span_days"] = (summary["last_date"] - summary["first_date"]).dt.days + 1
    summary["records_per_active_day"] = summary["records"] / summary["active_days"].replace(0, np.nan)
    return summary


def build_overall_stats(df: pd.DataFrame, numeric_cols: Iterable[str]) -> pd.DataFrame:
    rows = []
    for col in numeric_cols:
        s = df[col].dropna()
        if s.empty:
            continue
        rows.append({
            "metric": col,
            "total": s.sum(),
            "mean": s.mean(),
            "median": s.median(),
            "mode": safe_mode(s),
            "std": s.std(),
            "min": s.min(),
            "max": s.max(),
            "count": s.count(),
            "non_zero_count": (s != 0).sum(),
        })
    return pd.DataFrame(rows)


def daily_metric_frame(df: pd.DataFrame, metric: str, activity: str | None = None) -> pd.DataFrame:
    work = df.copy()
    # st.write(f"{activity=}, {metric=}")
    if activity and activity != "All activities":
        work = work[work["activity"] == activity]
    daily = work.groupby(work["date"].dt.normalize(), as_index=True).agg(
        value=(metric, "sum"),
        records=(metric, "count"),
    ).reset_index()  # .rename(columns={"value": "date"})
    # display_df(work, "work", hide_index=False, fail_safe=False)
    # display_df(daily, "daily", hide_index=False, fail_safe=False)
    if daily.empty:
        return daily
    # full_dates = pd.date_range(work["date"].min(), work["date"].max(), freq="D")
    full_dates = work["date"].dropna().unique()
    # display_df(full_dates, "full_dates", hide_index=False, fail_safe=False)
    # st.stop()
    daily = daily.set_index("date").reindex(full_dates).rename_axis("date").reset_index()
    daily["value"] = daily["value"].fillna(0)
    daily["records"] = daily["records"].fillna(0).astype(int)
    return daily


def build_trend_table(daily: pd.DataFrame, windows: Iterable[int] = ROLLING_WINDOWS) -> pd.DataFrame:
    if daily.empty:
        return pd.DataFrame()

    rows = []
    history_mean = daily["value"].mean()
    history_median = daily["value"].median()
    history_std = daily["value"].std()

    for window in windows:
        if len(daily) < window:
            continue
        recent = daily.tail(window)["value"]
        previous = daily.iloc[:-window]["value"]
        recent_mean = recent.mean()
        prev_mean = previous.mean() if not previous.empty else history_mean
        change = recent_mean - prev_mean
        pct_change = (change / prev_mean * 100) if prev_mean not in [0, np.nan] and pd.notna(prev_mean) and prev_mean != 0 else np.nan
        z_score = (recent_mean - history_mean) / history_std if pd.notna(history_std) and history_std != 0 else np.nan

        if pd.isna(pct_change):
            status = "No comparison"
        elif pct_change >= 10:
            status = "Improving"
        elif pct_change <= -10:
            status = "Declining"
        else:
            status = "Stable"

        rows.append({
            "window_days": window,
            "recent_avg_per_day": recent_mean,
            "previous_avg_per_day": prev_mean,
            "history_avg_per_day": history_mean,
            "history_median_per_day": history_median,
            "change_vs_previous": change,
            "pct_change_vs_previous": pct_change,
            "z_score_vs_history": z_score,
            "status": status,
        })
    return pd.DataFrame(rows)


# -----------------------------
# HTML cards
# -----------------------------
def metric_card(title: str, value: str, subtitle: str = "", status: str = "neutral") -> str:
    border = {
        "good": "#18a058",
        "bad": "#d03050",
        "neutral": "#6b7280",
        "warn": "#f0a020",
    }.get(status, "#6b7280")
    return f"""
    <div style="border-left: 6px solid {border}; padding: 1rem; border-radius: 0.85rem;
                background: rgba(250,250,250,0.06); box-shadow: 0 1px 8px rgba(0,0,0,0.10);
                min-height: 118px; margin-bottom: 0.8rem;">
        <div style="font-size:0.82rem; opacity:0.75; text-transform:uppercase; letter-spacing:0.04em;">{title}</div>
        <div style="font-size:1.85rem; font-weight:750; margin-top:0.25rem;">{value}</div>
        <div style="font-size:0.92rem; opacity:0.78; margin-top:0.25rem;">{subtitle}</div>
    </div>
    """


def render_cards(cards: list[tuple[str, str, str, str]], columns: int = 4) -> None:
    cols = st.columns(columns)
    for i, (title, value, subtitle, status) in enumerate(cards):
        with cols[i % columns]:
            st.markdown(metric_card(title, value, subtitle, status), unsafe_allow_html=True)


# -----------------------------
# Plotly charts
# -----------------------------
def add_stat_lines(fig: go.Figure, series: pd.Series, *, include_mode: bool = True) -> go.Figure:
    stats = {
        "Mean": series.mean(),
        "Median": series.median(),
        "Std +": series.mean() + series.std() if pd.notna(series.std()) else np.nan,
        "Std -": series.mean() - series.std() if pd.notna(series.std()) else np.nan,
    }
    if include_mode:
        stats["Mode"] = safe_mode(series)

    for label, value in stats.items():
        if pd.notna(value):
            dash = "dash" if label not in ["Mean", "Median"] else "dot"
            fig.add_hline(y=value, line_dash=dash, annotation_text=f"{label}: {fmt_value(value)}", annotation_position="top left")
    return fig


def metric_timeline_chart(daily: pd.DataFrame, metric: str, windows: Iterable[int]) -> go.Figure:
    fig = px.line(daily, x="date", y="value", markers=True, title=f"Daily {metric} with rolling averages")
    for window in windows:
        if len(daily) >= window:
            daily[f"rolling_{window}d"] = daily["value"].rolling(window, min_periods=max(2, window // 2)).mean()
            fig.add_trace(go.Scatter(
                x=daily["date"], y=daily[f"rolling_{window}d"], mode="lines", name=f"{window}d avg"
            ))
    add_stat_lines(fig, daily["value"], include_mode=False)
    fig.update_layout(hovermode="x unified", legend_title_text="Series")
    return fig


def histogram_chart(df: pd.DataFrame, metric: str) -> go.Figure:
    fig = px.histogram(df, x=metric, nbins=30, marginal="box", title=f"Distribution of {metric}")
    mean_v = df[metric].mean()
    median_v = df[metric].median()
    mode_v = safe_mode(df[metric])
    for label, value in {"Mean": mean_v, "Median": median_v, "Mode": mode_v}.items():
        if pd.notna(value):
            fig.add_vline(x=value, line_dash="dash", annotation_text=f"{label}: {fmt_value(value)}")
    return fig


def activity_comparison_chart(df: pd.DataFrame, metric: str, agg: str) -> go.Figure:
    grouped = df.groupby(["activity", "unit"], dropna=False)[metric].agg(agg).reset_index()
    grouped["activity_unit"] = grouped["activity"].astype(str) + np.where(grouped["unit"].astype(str).eq(""), "", " (" + grouped["unit"].astype(str) + ")")
    grouped = grouped.sort_values(metric, ascending=False)
    fig = px.bar(grouped, x="activity_unit", y=metric, title=f"{agg.title()} {metric} by activity")
    fig.update_layout(xaxis_title="Activity", yaxis_title=f"{agg.title()} {metric}")
    return fig


def heatmap_chart(df: pd.DataFrame, metric: str) -> go.Figure:
    work = df.copy()
    work["weekday"] = work["date"].dt.day_name()
    work["week"] = work["date"].dt.to_period("W").astype(str)
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    pivot = work.pivot_table(index="weekday", columns="week", values=metric, aggfunc="sum").reindex(weekday_order)
    fig = px.imshow(pivot, aspect="auto", title=f"{metric} frequency/intensity heatmap by week and weekday")
    return fig


# -----------------------------
# Dashboard
# -----------------------------
def main() -> None:
    st.title("Activity Analytics Dashboard")
    st.caption("Summaries, rolling trends, and performance comparisons from data.xlsx")
    
    with st.sidebar:
        st.header("Controls")
        with st.container(border=True):
            sah = st.radio("Seconds as?", ["d", "h", "m", "s"], 2, horizontal=True)
        
    try:
        df = load_data(seconds_as_hours=sah)
    except Exception as exc:
        st.error(f"Could not load data: {exc}")
        st.stop()

    numeric_cols = get_numeric_columns(df)
    if not numeric_cols:
        st.error("No numeric columns were found to analyze.")
        st.stop()

    activities = ["All activities"] + sorted(df["activity"].dropna().astype(str).unique().tolist())

    with st.sidebar:
        selected_activity = st.selectbox("Activity", activities)
        default_metric = "times" if "times" in numeric_cols else numeric_cols[0]
        selected_metric = st.selectbox("Metric", numeric_cols, index=numeric_cols.index(default_metric))
        selected_agg = st.selectbox("Comparison aggregation", ["sum", "mean", "median", "max", "count", "std"], index=0)
        selected_windows = st.multiselect("Rolling windows", ROLLING_WINDOWS, default=[7, 14, 31, 62])

    filtered = df if selected_activity == "All activities" else df[df["activity"].astype(str) == selected_activity]
    # display_df(filtered, "filtered")
    daily = daily_metric_frame(df, selected_metric, selected_activity)
    trend = build_trend_table(daily, selected_windows)

    total_records = len(filtered)
    active_days = filtered["date"].dt.normalize().nunique()
    metric_total = filtered[selected_metric].sum()
    metric_mean = filtered[selected_metric].mean()
    metric_median = filtered[selected_metric].median()
    metric_std = filtered[selected_metric].std()
    top_row = filtered.loc[filtered[selected_metric].idxmax()] if not filtered.empty and filtered[selected_metric].notna().any() else None

    best_trend = None
    if not trend.empty:
        best_trend = trend.iloc[trend["pct_change_vs_previous"].fillna(-np.inf).idxmax()]

    cards = [
        ("Records", fmt_value(total_records), f"Across {fmt_value(active_days)} active days", "neutral"),
        (f"Total {selected_metric}", fmt_value(metric_total), f"Mean {fmt_value(metric_mean)} | Median {fmt_value(metric_median)}", "neutral"),
        ("Consistency", fmt_value(metric_std), "Standard deviation", "neutral"),
        (
            "Best recent trend",
            "—" if best_trend is None else f"{fmt_value(best_trend['pct_change_vs_previous'])}%",
            "No trend yet" if best_trend is None else f"{int(best_trend['window_days'])}d window: {best_trend['status']}",
            "neutral" if best_trend is None else ("good" if best_trend["status"] == "Improving" else "bad" if best_trend["status"] == "Declining" else "warn"),
        ),
    ]
    render_cards(cards)

    if top_row is not None:
        st.info(
            f"Top single record for **{selected_metric}**: **{fmt_value(top_row[selected_metric])}** "
            f"on **{pd.to_datetime(top_row['date']).strftime('%Y-%m-%d')}** "
            f"for **{top_row['activity']}** {f'({top_row["unit"]})' if str(top_row.get('unit', '')) else ''}."
        )

    cols = st.columns([0.15, 0.85])
    improve_status = None
    with cols[1]:
        if trend.empty:
            st.warning("Not enough daily data for the selected rolling windows yet.")
        else:
            improving = trend[trend["status"] == "Improving"]
            declining = trend[trend["status"] == "Declining"]
            if not improving.empty:
                row = improving.sort_values("pct_change_vs_previous", ascending=False).iloc[0]
                improve_status = 1
                st.success(
                    f"You are improving most over the **{int(row['window_days'])}-day** window: "
                    f"recent average is **{fmt_value(row['pct_change_vs_previous'])}%** above the prior baseline."
                )
            if not declining.empty:
                row = declining.sort_values("pct_change_vs_previous").iloc[0]
                improve_status = -1
                st.error(
                    f"The weakest recent area is the **{int(row['window_days'])}-day** window: "
                    f"recent average is **{fmt_value(row['pct_change_vs_previous'])}%** below the prior baseline."
                )
            if improving.empty and declining.empty:
                improve_status = 0
                st.info("Performance looks broadly stable for the selected windows.")
                
    with cols[0]:
        msg = "Improving?"
        if improve_status == 1:
            st.success(msg)
        elif improve_status == 0:
            st.info(msg)
        elif improve_status == -1:
            st.error(msg)
        else:
            st.warning(msg)

    tab_overview, tab_trends, tab_compare, tab_stats, tab_data = st.tabs([
        "Overview", "Rolling Trends", "Activity Comparison", "Stats", "Data"
    ])

    with tab_overview:
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(metric_timeline_chart(daily, selected_metric, selected_windows), use_container_width=True)
        with c2:
            st.plotly_chart(histogram_chart(filtered, selected_metric), use_container_width=True)
        with st.expander("Weekday / weekly heatmap", expanded=False):
            st.plotly_chart(heatmap_chart(filtered, selected_metric), use_container_width=True)

    with tab_trends:
        if not trend.empty:
            trend_display = trend.copy()
            trend_display["pct_change_vs_previous"] = trend_display["pct_change_vs_previous"].round(2)
            trend_display["z_score_vs_history"] = trend_display["z_score_vs_history"].round(2)
            display_df(trend_display, "Rolling window performance vs previous history")

            fig = px.bar(
                trend,
                x="window_days",
                y="pct_change_vs_previous",
                color="status",
                text=trend["pct_change_vs_previous"].round(1),
                title=f"Rolling-window trend for {selected_metric}",
            )
            fig.add_hline(y=0, line_dash="dash")
            fig.update_layout(xaxis_title="Window days", yaxis_title="% change vs previous baseline")
            st.plotly_chart(fig, use_container_width=True)

    with tab_compare:
        st.plotly_chart(activity_comparison_chart(df, selected_metric, selected_agg), use_container_width=True)
        with st.expander("Full activity summary table", expanded=False):
            activity_summary = build_activity_summary(df, numeric_cols)
            display_df(activity_summary, "Activity summary")

    with tab_stats:
        stats = build_overall_stats(filtered, numeric_cols)
        display_df(stats, "Overall metric statistics")
        selected_stats = stats[stats["metric"] == selected_metric]
        if not selected_stats.empty:
            row = selected_stats.iloc[0]
            stat_cards = [
                ("Mean", fmt_value(row["mean"]), "Average value", "neutral"),
                ("Median", fmt_value(row["median"]), "Middle value", "neutral"),
                ("Mode", fmt_value(row["mode"]), "Most common value", "neutral"),
                ("Stdv", fmt_value(row["std"]), "Spread / consistency", "neutral"),
            ]
            render_cards(stat_cards)

    with tab_data:
        display_df(
            filtered,
            "Filtered master data",
            totals=["mean", "sum", "std", "var", "min", "max"],
            fail_safe=False
        )
        with st.expander("Data quality checks", expanded=False):
            quality = pd.DataFrame({
                "column": df.columns,
                "dtype": [str(df[c].dtype) for c in df.columns],
                "missing": [df[c].isna().sum() for c in df.columns],
                "missing_pct": [df[c].isna().mean() * 100 for c in df.columns],
                "unique_values": [df[c].nunique(dropna=True) for c in df.columns],
            })
            display_df(quality, "Data quality")


if __name__ == "__main__":
    main()
