from calpads.client import CALPADSClient
import getpass

# https://summit-public-schools.gitbook.io/calpads-api

district_codes = [
    "0973783",  # black oak mine
    "0961838",  # buckeye
    "0961846",  # camino
    "0910090",  # edcoe
    "0961853",  # el dorado high
    "0961879",  # gold oak
    "0961887",  # gold trail
    "0961895",  # indian diggings
    "0961903",  # lake tahoe
    "0961911",  # latrobe
    "0961929",  # mother lode
    "0961945",  # pioneer
    "0961952",  # placerville
    "0961960",  # pollock
    "0961978",  # rescue
    "0961986",  # silverfork
]


# log in to calpads using your username and getpass.getpass()
cc = CALPADSClient(
    username=input("Enter CALPADS username:\n"),
    password=getpass.getpass("Enter CALPADS password:\n"),
)


for lea in district_codes:

    dry = cc.download_report(lea_code=lea, report_code="1.3", dry_run=True)

    form_input = {
        "AcademicYear": "2024-2025",
        "AsOfMonth": "October",
        "AsOfDay": "4",
        "LEA": dry["LEA"][0],
        "Schooltypecodevalue": {
            key: True for key, _ in dry["Schooltypecodevalue"].items()
        },
        "SchoolName": {key: True for key, _ in dry["SchoolName"].items()},
        "Grade": {key: True for key, _ in dry["Grade"].items()},
        "Gender": {key: True for key, _ in dry["Gender"].items()},
        "Race": {key: True for key, _ in dry["Race"].items()},
        "TitleIIIEligibleImmigrant": {
            key: True for key, _ in dry["TitleIIIEligibleImmigrant"].items()
        },
        "EnglishLanguageAcquisitionstatus": {
            key: True for key, _ in dry["EnglishLanguageAcquisitionstatus"].items()
        },
        "TitleIpartCMigrant": {
            key: True for key, _ in dry["TitleIpartCMigrant"].items()
        },
        "Socioeconomicaldis": {
            key: True for key, _ in dry["Socioeconomicaldis"].items()
        },
        "Specialeducation": {key: True for key, _ in dry["Specialeducation"].items()},
        "GiftedandTalented": {key: True for key, _ in dry["GiftedandTalented"].items()},
        "InterdistrictTransfer": {
            key: True for key, _ in dry["InterdistrictTransfer"].items()
        },
        "EsiIdGeographicRsdncDistKey": {
            key: True for key, _ in dry["EsiIdGeographicRsdncDistKey"].items()
        },
        "GroupBy": "Grade",
    }

    dry = cc.download_report(
        lea_code=lea,
        report_code="1.3",
        file_name=f"enrollData/Enrollment_{lea}.csv",
        form_data=form_input,
    )
