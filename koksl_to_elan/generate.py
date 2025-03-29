def to_ann_tags(tier_id, anns):

    def to_tag(ann):
        ann_id = ann["ann_id"]
        slot_ref1 = ann["slot_ref1"]
        slot_ref2 = ann["slot_ref2"]
        ann_value = ann["ann_value"]
        return f"""    <ANNOTATION>
            <ALIGNABLE_ANNOTATION ANNOTATION_ID="{ann_id}"
                TIME_SLOT_REF1="{slot_ref1}" TIME_SLOT_REF2="{slot_ref2}">
                <ANNOTATION_VALUE>{ann_value}</ANNOTATION_VALUE>
            </ALIGNABLE_ANNOTATION>
        </ANNOTATION>"""

    delim = f"\n{'    '}"
    tags = [*map(to_tag, anns)]

    return f"""<TIER LINGUISTIC_TYPE_REF="default-lt" TIER_ID="{tier_id}">
    {delim.join(tags)}
    </TIER>"""


def nms_by_type(nms):

    def by_type(nms_type_anns):
        nms_type, anns = nms_type_anns
        return to_ann_tags(nms_type, anns)

    delim = f"\n{'    '}"

    return delim.join([*map(by_type, nms.items())])


def to_time_slot_tags(slots):

    def to_tag(val_id):
        val, id = val_id
        return f'<TIME_SLOT TIME_SLOT_ID="{id}" TIME_VALUE="{val}"/>'

    delim = f"\n{'        '}"
    tags = [*map(to_tag, slots)]

    return delim.join(tags)


def to_eaf(media_url, obj):
    time_slot_tags = to_time_slot_tags(obj["time_slots"])
    ko = to_ann_tags("Korean", obj["ko"])
    ksl_simple = to_ann_tags("KSL_simple", obj["ksl_simple"])
    ms_strong = to_ann_tags("ms_strong", obj["ms_strong"])
    ms_weak = to_ann_tags("ms_weak", obj["ms_weak"])
    nms = nms_by_type(obj["nms"])

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<ANNOTATION_DOCUMENT AUTHOR="" DATE=""
    FORMAT="3.0" VERSION="3.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://www.mpi.nl/tools/elan/EAFv3.0.xsd">
    <HEADER MEDIA_FILE="" TIME_UNITS="milliseconds">
        <MEDIA_DESCRIPTOR
            MEDIA_URL="{media_url}"
            MIME_TYPE="video/mp4"/>
    </HEADER>
    <TIME_ORDER>
        {time_slot_tags}
    </TIME_ORDER>
    {ko}
    {ksl_simple}
    {ms_strong}
    {ms_weak}
    {nms}
    <LINGUISTIC_TYPE GRAPHIC_REFERENCES="false"
        LINGUISTIC_TYPE_ID="default-lt" TIME_ALIGNABLE="true"/>
    <CONSTRAINT
        DESCRIPTION="Time subdivision of parent annotation's time interval, no time gaps allowed within this interval" STEREOTYPE="Time_Subdivision"/>
    <CONSTRAINT
        DESCRIPTION="Symbolic subdivision of a parent annotation. Annotations refering to the same parent are ordered" STEREOTYPE="Symbolic_Subdivision"/>
    <CONSTRAINT DESCRIPTION="1-1 association with a parent annotation" STEREOTYPE="Symbolic_Association"/>
    <CONSTRAINT
        DESCRIPTION="Time alignable annotations within the parent annotation's time interval, gaps are allowed" STEREOTYPE="Included_In"/>
</ANNOTATION_DOCUMENT>

"""


"""<?xml version="1.0" encoding="UTF-8"?>
<ANNOTATION_DOCUMENT AUTHOR="" DATE=""
    FORMAT="3.0" VERSION="3.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://www.mpi.nl/tools/elan/EAFv3.0.xsd">
    <HEADER MEDIA_FILE="" TIME_UNITS="milliseconds">
        <MEDIA_DESCRIPTOR
            MEDIA_URL="file:///C:/Users/yeon/Hobbiton/koksl-to-elan/sample/mp4/SCUSHPAKOKSL2200000001.mp4"
            MIME_TYPE="video/mp4"/>
    </HEADER>
    <TIME_ORDER>
        <TIME_SLOT TIME_SLOT_ID="ts1" TIME_VALUE="460"/>
        <TIME_SLOT TIME_SLOT_ID="ts2" TIME_VALUE="740"/>
        <TIME_SLOT TIME_SLOT_ID="ts3" TIME_VALUE="920"/>
        <TIME_SLOT TIME_SLOT_ID="ts4" TIME_VALUE="920"/>
        <TIME_SLOT TIME_SLOT_ID="ts5" TIME_VALUE="1320"/>
        <TIME_SLOT TIME_SLOT_ID="ts6" TIME_VALUE="1320"/>
        <TIME_SLOT TIME_SLOT_ID="ts7" TIME_VALUE="1580"/>
        <TIME_SLOT TIME_SLOT_ID="ts8" TIME_VALUE="2140"/>
    </TIME_ORDER>
    <TIER LINGUISTIC_TYPE_REF="default-lt" TIER_ID="tier1">
        <ANNOTATION>
            <ALIGNABLE_ANNOTATION ANNOTATION_ID="a1"
                TIME_SLOT_REF1="ts1" TIME_SLOT_REF2="ts2">
                <ANNOTATION_VALUE>사랑</ANNOTATION_VALUE>
            </ALIGNABLE_ANNOTATION>
        </ANNOTATION>
        <ANNOTATION>
            <ALIGNABLE_ANNOTATION ANNOTATION_ID="a2"
                TIME_SLOT_REF1="ts3" TIME_SLOT_REF2="ts5">
                <ANNOTATION_VALUE>이다</ANNOTATION_VALUE>
            </ALIGNABLE_ANNOTATION>
        </ANNOTATION>
    </TIER>
    <TIER LINGUISTIC_TYPE_REF="default-lt" TIER_ID="tier2">
        <ANNOTATION>
            <ALIGNABLE_ANNOTATION ANNOTATION_ID="a3"
                TIME_SLOT_REF1="ts4" TIME_SLOT_REF2="ts6">
                <ANNOTATION_VALUE>이다</ANNOTATION_VALUE>
            </ALIGNABLE_ANNOTATION>
        </ANNOTATION>
        <ANNOTATION>
            <ALIGNABLE_ANNOTATION ANNOTATION_ID="a4"
                TIME_SLOT_REF1="ts7" TIME_SLOT_REF2="ts8">
                <ANNOTATION_VALUE>하루</ANNOTATION_VALUE>
            </ALIGNABLE_ANNOTATION>
        </ANNOTATION>
    </TIER>
    <LINGUISTIC_TYPE GRAPHIC_REFERENCES="false"
        LINGUISTIC_TYPE_ID="default-lt" TIME_ALIGNABLE="true"/>
    <CONSTRAINT
        DESCRIPTION="Time subdivision of parent annotation's time interval, no time gaps allowed within this interval" STEREOTYPE="Time_Subdivision"/>
    <CONSTRAINT
        DESCRIPTION="Symbolic subdivision of a parent annotation. Annotations refering to the same parent are ordered" STEREOTYPE="Symbolic_Subdivision"/>
    <CONSTRAINT DESCRIPTION="1-1 association with a parent annotation" STEREOTYPE="Symbolic_Association"/>
    <CONSTRAINT
        DESCRIPTION="Time alignable annotations within the parent annotation's time interval, gaps are allowed" STEREOTYPE="Included_In"/>
</ANNOTATION_DOCUMENT>

"""
