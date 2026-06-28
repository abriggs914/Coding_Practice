import datetime
import pandas as pd
from docx import Document
from itertools import zip_longest

doc = Document(r"C:\Users\abrig\Documents\Coding_Practice\Python\Resume Building\2026\jobs applied to.docx")

table = doc.tables[0]

data = [
    [cell.text.strip() for cell in row.cells]
    for row in table.rows
]

headers = data[0]
rows = data[1:]

df_jobs = pd.DataFrame(rows, columns=headers)
for c in ["Date", "InterviewDate"]:
    df_jobs[c] = pd.to_datetime(df_jobs[c])

print(df_jobs)

date_lo = datetime.date(2026, 2, 26)

today = datetime.datetime.now().date()


def report(text, val, fc=".", rjl1=30, rjl2=12, fmt=None):
    if fmt == "percent":
        return f"{text}".ljust(rjl1, fc) + f"{val:.3f}%".rjust(rjl2)
    if fmt == "date":
        return f"{text}".ljust(rjl1, fc) + f"{val:%Y-%m-%d}".rjust(rjl2)
    elif fmt is not None:
        return f"{text}".ljust(rjl1, fc) + (f"{val:{fmt}}".rjust(rjl2) if val is not None else "None")
    else:
        return f"{text}".ljust(rjl1, fc) + f"{val}".rjust(rjl2)


def report_df(df, title=None, rtype="str"):
    
    fmts = {
        f"Jobs applied to per day:": ".3f",
        f"Days between application:": ".3f",
        f"Interviews per application:": ".3f",
        f"Applications per interview:":".3f",
        f"First date:": "date",
        f"Last date:": "date",
    }
    border = "\n" + ("\n".join(["#"*42 for _ in range(3)])) + "\n"
    
    if isinstance(df, (list, tuple)):
        if not df:
            return
        
        res = []
        for i in range(len(df) - 1):
            a, b = df[i], df[i + 1]
            ra = report_df(a, f"{i}_A", rtype="dict")
            rb = report_df(b, f"{i}_B", rtype="dict")
            dd = []
            for k in set(ra.keys()).union(set(rb.keys())):
                va, vb = ra.get(k, 0), rb.get(k, 0)
                va = va if va is not None else 0
                vb = vb if vb is not None else 0
                d = vb - va
                f = fmts.get(k)
                if f == "date":
                    f = None
                dd.append(report(k, d, fmt=f))
            # print(f"{dd=}")
            res.append(dd.copy())
        
        return [border + f"\n\n\t{title}\n" + ("\n".join(d)) for d in res]
                
    else:

        date_diff = (df["Date"].max().date() - df["Date"].min().date()).days
        days_since_last_application = (today - df["Date"].max().date()).days
        days_since_last_interview = (today - df["InterviewDate"].max().date()).days if df["InterviewDate"].dropna().tolist() else None
        jatpd = len(df) / date_diff
        companies =  df["Company"].unique().tolist()

        df_dev_positions = df[df["Position"].str.lower().str.contains("dev")]
        df_analyst_positions = df[df["Position"].str.lower().str.contains("analy")]
        df_remote_positions = df[df["Location"].str.lower().str.contains("remote")]
        df_interview_positions = df[~pd.isna(df["InterviewDate"])]
        
        txts = [border]
        if title:
            txts.append(f"\n\t{title}")
        if rtype != "str":
             txts = {}
        for t, v in [
            (f"Total days:", date_diff),
            (f"Total applications:", len(df)),
            (f"# Interviews:", len(df_interview_positions)),
            (f"# Companies:", len(companies)),
            (f"# Dev jobs:", len(df_dev_positions)),
            (f"# Analyst jobs:", len(df_analyst_positions)),
            (f"# Remote jobs:", len(df_remote_positions)),
            (f"Jobs applied to per day:", jatpd),
            (f"Days between application:", 1/jatpd),
            (f"Interviews per application:", len(df_interview_positions) / len(df)),
            (f"Applications per interview:", (len(df) / (len(df_interview_positions))) if not df_interview_positions.empty else None),
            (f"Days since last application:", days_since_last_application),
            (f"Days since last interview:", days_since_last_interview),
            (f"First date:", df["Date"].min()),
            (f"Last date:", df["Date"].max()),
        ]:
            f = {"fmt": fmts.get(t)}
            if rtype != "str":
                txts[t] = v
            else:
                txts.append(report(t, v, **f))
        
        return txts if (rtype != "str") else "\n".join(txts)
    
        
def text_grid(texts, max_width=480, delim=" | "):
    texts = [str(t).replace("\t", "    ") for t in texts]
    ztexts = list(zip_longest(*map(lambda t: t.split("\n"), texts)))
    max_w = [max([len(str(ztexts[j][i])) for j in range(len(ztexts))]) for i in range(len(texts))]
    
    res = ""
    n_cols = len(max_w)
    nc = int((max_width - (len(delim) * (len(texts) - 1))) / n_cols)
    for i in range(len(ztexts)):
        txts = ztexts[i]
        for j, txt in enumerate(txts):
            rt = (f"{delim}" if 0 < j < len(txts) else "") + (str(txt) if txt else "").ljust(min(nc, max_w[j]))
            rt = rt if len(rt.removeprefix(delim)) <= nc else (rt[:nc-4] + " ...")
            res += rt[:nc]
        res += "\n"
    
    return res
       
       
df_1 = df_jobs.copy()
df_2 = df_jobs[df_jobs["Date"].dt.date > date_lo]
df_3 = df_jobs[df_jobs["Date"].dt.date < date_lo]
r1 = report_df(df_1, f"All data:")
r3 = report_df(df_3, f"Before LO:")
r2 = report_df(df_2, f"Since LO:")

pd.merge_asof
r2_r3 = report_df([df_2, df_3], rtype="list", title="Change from Before LO and After:")
tg = text_grid([r1, r2, r3, r2_r3[0]])
print(tg)