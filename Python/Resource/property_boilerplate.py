#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

VERSION = \
    """    
        Functions to write property boilerplate.
        Version.............................1.03
        Date..........................2022-09-12
        Author......................Avery Briggs
    """


def VERSION_NUMBER():
    return float(VERSION.split("\n")[2].split(".")[-2] + "." + VERSION.split("\n")[2].split(".")[-1])


def VERSION_DATE():
    return VERSION.split("\n")[3].split(".")[-1]


def VERSION_AUTHOR():
    return VERSION.split("\n")[4].split(".")[-1]


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

def getter(x):
    name = x.replace("self.", "")
    name = name[1:] if name.startswith("_") else name
    return f"""def get_{name}(self):\n\treturn self._{name}"""


def setter(x):
    name = x.replace("self.", "")
    name = name[1:] if name.startswith("_") else name
    return f"""def set_{name}(self, {name}_in):\n\tself._{name} = {name}_in"""


def delter(x):
    name = x.replace("self.", "")
    name = name[1:] if name.startswith("_") else name
    return f"""def del_{name}(self):\n\tdel self._{name}"""


def proter(x):
    name = x.replace("self.", "")
    name = name[1:] if name.startswith("_") else name
    return f"""{name} = property(get_{name}, set_{name}, del_{name})"""


def property_boilerplate(class_in, output_file="./boilerplate_output.txt", do_export=True):
    lst = list(class_in.__dict__.keys())
    lst.sort()

    lines = ""
    for name in lst:
        lines += f"\n# {name}\n{getter(name)}\n{setter(name)}\n{delter(name)}\n"
    for name in lst:
        lines += f"\n{proter(name)}"

    if do_export:
        print("Writing to file...")
        with open(output_file, "w") as fo:
            fo.write(lines)
        print("File written to successfully!")
    else:
        print(lines)
    return lines


if __name__ == "__main__":
    lst = [
        'self.prod_sched_v2_id',
        'self.quote_v2',
        'self.wo_num_v2',
        'self.job_start_date_v2',
        'self.job_finish_date_v2',
        'self.dtprodschedv2ts',
        'self.job_start_line_v2',
        'self.hide_from_prod_input_v2',
        'self.InputField1_v2',
        'self.InputField2_v2',
        'self.ApplyUpdate_v2',
        'self.ApplyUpdateUser_v2',

        'self.prod_sched_id',
        'self.quote',
        'self.wo_num',
        'self.InputField1',
        'self.InputField2',
        'self.Beam_Line',
        'self.Beam_Date',
        'self.GN_Line',
        'self.GN_Date',
        'self.WO_Line_1',
        'self.Prod_Date_1',
        'self.WO_Line_2',
        'self.Prod_Date_2',
        'self.Other',
        'self.Other_Line',
        'self.Other_Date',
        'self.HideFromProdInput',
        'self.Step1SYSPROBudget',
        'self.Step2SYSPROBudget',
        'self.dtprodschedts',
        'self.ApplyUpdate',
        'self.ApplyUpdateUser',
        'self.Slot',
        'self.Slot_Quote',
        'self.Slot_Approved',
        'self.Prod_On',
        'self.Prod_On_Time',
        'self.Prod_Off',
        'self.Prod_Off_Time',
        'self.Prod_PM',
        'self.Prod_Complete',
        'self.Prod2_On',
        'self.Prod2_On_Time',
        'self.Prod2_Off',
        'self.Prod2_Off_Time',
        'self.Prod2_PM',
        'self.Prod2_Complete',
        'self.Prod_Instructions',
        'self.Beam_On',
        'self.Beam_Off',
        'self.Beam_Complete',
        'self.Beam_PM',
        'self.Beam_Instructions',
        'self.GN_On',
        'self.GN_Off',
        'self.GN_Complete',
        'self.GN_PM',
        'self.GN_Instructions',
        'self.Axle',
        'self.Axle_On',
        'self.Axle_Off',
        'self.Axle_Complete',
        'self.Axle_PM',
        'self.Axle_Instructions',
        'self.Other_On',
        'self.Other_On_Time',
        'self.Other_Off',
        'self.Other_Off_Time',
        'self.Other_Complete',
        'self.Other_PM',
        'self.Other_Instructions',
        'self.Stargate_WO',
        'self.OrderID',
        'self.SGQuote',
        'self.Quote_Date',
        'self.Order_Date',
        'self.WO',
        'self.Sales_Order',
        'self.Model_No',
        'self.Width',
        'self.Spread',
        'self.DealerID',
        'self.Sale_PersonID',
        'self.Price',
        'self.Prom_Drawing',
        'self.Special_Instructions',
        'self.Date_Declined',
        'self.Decline_Rejected',
        'self.Serial_Number',
        'self.Available_Date',
        'self.Delivery_Date',
        'self.Requested_Delivery_Date',
        'self.Finish_Date',
        'self.Purchase_Order',
        'self.PO_Date',
        'self.PayID',
        'self.Volume_Discount',
        'self.Program_Discount',
        'self.Discount1_Name',
        'self.Discount1_Type',
        'self.Discount1',
        'self.Discount2_Name',
        'self.Discount2_Type',
        'self.Discount2',
        'self.Discount3_Name',
        'self.Discount3_Type',
        'self.Discount3',
        'self.Est_Pro_Date',
        'self.Notes',
        'self.EngNotes',
        'self.CarrierID',
        'self.CustID',
        'self.US_Sale',
        'self.Shipped_Date',
        'self.GL_Override_Date',
        'self.FE_Rate',
        'self.PDD',
        'self.Deck_Length',
        'self.Invoice',
        'self.Date_Registered',
        'self.Date_In_Service',
        'self.Invoice_Date',
        'self.Date_Requested',
        'self.GVWR',
        'self.Tare',
        'self.Selection',
        'self.Warranty',
        'self.BWSPaid',
        'self.BWSPaidDate',
        'self.CommPaid',
        'self.CommPaidDate',
        'self.ts_timestamp',
        'self.ModifiedBy',

        'self.Lead_Date',
        'self.Lead_Source',
        'self.LeadID',
        'self.DealerBranchID',
        'self.DealerSalesPersonID',
        'self.DataEntryCheck',
        'self.DataEntryUser',
        'self.FinishedGoodsDealerLocID',
        'self.WO_Reviewed',
        'self.WO_Review_Date',
        'self.Follow_Up_Date',
        'self.MSOIsDifferent',
        'self.MSOLocID',
        'self.EstInvDateOverride',
        'self.Estimated_Invoice_Date',
        'self.AdditionalPricingInfo',
        'self.Slot_Orders',
        'self.TempModel',
        'self.HighRiskUnit',
        'self.EngNotes_V2',
        'self.CompanyID',
        'self.Customer_WO',
        'self.PriceSecured',
        'self.DateSecured',
        'self.SecuredBy'
    ]

    f = "./output.txt"
    with open(f, "w") as fo:
        for name in lst:
            fo.write(f"\n# {name}\n{getter(name)}\n{setter(name)}\n{delter(name)}\n")
        for name in lst:
            fo.write(f"\n{proter(name)}")

    # known class example
    from dataclasses import dataclass


    @dataclass
    class Foo:
        id_num: int
        name: str
        age: int
        height: float


    f1 = Foo(1, "1", 1, 1.0)
    property_boilerplate(f1)
