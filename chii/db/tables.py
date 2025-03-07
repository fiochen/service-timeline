import zlib
import datetime
from typing import TYPE_CHECKING, Any, List, Tuple, Union, Optional

from sqlalchemy import TIMESTAMP, Date, Enum, Float, Index, Table, Column, String, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.mysql import (
    CHAR,
    ENUM,
    TEXT,
    YEAR,
    INTEGER,
    TINYINT,
    VARCHAR,
    SMALLINT,
    MEDIUMINT,
    MEDIUMBLOB,
    MEDIUMTEXT,
)

from chii.compat import phpseralize
from chii.compat.phpseralize import dict_to_list

Base = declarative_base()
metadata = Base.metadata


class ChiiCharacter(Base):
    __tablename__ = "chii_characters"

    crt_id = Column(MEDIUMINT(8), primary_key=True)
    crt_name = Column(String(255, "utf8_unicode_ci"), nullable=False)
    crt_role = Column(TINYINT(4), nullable=False, index=True, comment="角色，机体，组织。。")
    crt_infobox: str = Column(MEDIUMTEXT, nullable=False)
    crt_summary: str = Column(MEDIUMTEXT, nullable=False)
    crt_img = Column(String(255, "utf8_unicode_ci"), nullable=False)
    crt_comment = Column(MEDIUMINT(9), nullable=False, server_default=text("'0'"))
    crt_collects = Column(MEDIUMINT(8), nullable=False)
    crt_dateline = Column(INTEGER(10), nullable=False)
    crt_lastpost = Column(INTEGER(11), nullable=False)
    crt_lock = Column(
        TINYINT(4), nullable=False, index=True, server_default=text("'0'")
    )
    crt_img_anidb = Column(VARCHAR(255), nullable=False)
    crt_anidb_id = Column(MEDIUMINT(8), nullable=False)
    crt_ban = Column(TINYINT(3), nullable=False, index=True, server_default=text("'0'"))
    crt_redirect = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
    crt_nsfw = Column(TINYINT(1), nullable=False)


class ChiiCrtCastIndex(Base):
    __tablename__ = "chii_crt_cast_index"

    crt_id = Column(MEDIUMINT(9), primary_key=True, nullable=False)
    prsn_id: int = Column(MEDIUMINT(9), primary_key=True, nullable=False, index=True)
    subject_id: int = Column(MEDIUMINT(9), primary_key=True, nullable=False, index=True)
    subject_type_id: int = Column(
        TINYINT(3), nullable=False, index=True, comment="根据人物归类查询角色，动画，书籍，游戏"
    )
    summary = Column(
        String(255, "utf8_unicode_ci"), nullable=False, comment="幼年，男乱马，女乱马，变身形态，少女形态。。"
    )


class ChiiCrtSubjectIndex(Base):
    __tablename__ = "chii_crt_subject_index"

    crt_id = Column(MEDIUMINT(9), primary_key=True, nullable=False)
    subject_id = Column(MEDIUMINT(9), primary_key=True, nullable=False, index=True)
    subject_type_id = Column(TINYINT(4), nullable=False, index=True)
    crt_type: int = Column(TINYINT(4), nullable=False, index=True, comment="主角，配角")
    ctr_appear_eps = Column(MEDIUMTEXT, nullable=False, comment="可选，角色出场的的章节")
    crt_order = Column(TINYINT(3), nullable=False)


class ChiiEpRevision(Base):
    __tablename__ = "chii_ep_revisions"
    __table_args__ = (Index("rev_sid", "rev_sid", "rev_creator"),)

    ep_rev_id = Column(MEDIUMINT(8), primary_key=True)
    rev_sid = Column(MEDIUMINT(8), nullable=False)
    rev_eids = Column(String(255), nullable=False)
    rev_ep_infobox = Column(MEDIUMTEXT, nullable=False)
    rev_creator = Column(MEDIUMINT(8), nullable=False)
    rev_version = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    rev_dateline = Column(INTEGER(10), nullable=False)
    rev_edit_summary = Column(String(200), nullable=False)


class ChiiEpisode(Base):
    __tablename__ = "chii_episodes"
    __table_args__ = (Index("ep_subject_id_2", "ep_subject_id", "ep_ban", "ep_sort"),)

    ep_id = Column(MEDIUMINT(8), primary_key=True)
    ep_subject_id = Column(MEDIUMINT(8), nullable=False, index=True)
    ep_sort = Column(Float, nullable=False, index=True, server_default=text("'0'"))
    ep_type = Column(TINYINT(1), nullable=False)
    ep_disc = Column(
        TINYINT(3),
        nullable=False,
        index=True,
        server_default=text("'0'"),
        comment="碟片数",
    )
    ep_name = Column(String(80), nullable=False)
    ep_name_cn = Column(String(80), nullable=False)
    ep_rate = Column(TINYINT(3), nullable=False)
    ep_duration = Column(String(80), nullable=False)
    ep_airdate = Column(String(80), nullable=False)
    ep_online = Column(MEDIUMTEXT, nullable=False)
    ep_comment = Column(MEDIUMINT(8), nullable=False)
    ep_resources = Column(MEDIUMINT(8), nullable=False)
    ep_desc = Column(MEDIUMTEXT, nullable=False)
    ep_dateline = Column(INTEGER(10), nullable=False)
    ep_lastpost = Column(INTEGER(10), nullable=False, index=True)
    ep_lock = Column(TINYINT(3), nullable=False, server_default=text("'0'"))
    ep_ban = Column(TINYINT(3), nullable=False, index=True, server_default=text("'0'"))


class ChiiMemberfield(Base):
    __tablename__ = "chii_memberfields"

    uid = Column(MEDIUMINT(8), primary_key=True, server_default=text("'0'"))
    site = Column(VARCHAR(75), nullable=False, server_default=text("''"))
    location = Column(VARCHAR(30), nullable=False, server_default=text("''"))
    bio = Column(TEXT, nullable=False)
    privacy = Column(MEDIUMTEXT, nullable=False)
    blocklist = Column(MEDIUMTEXT, nullable=False)


class ChiiMember(Base):
    __tablename__ = "chii_members"

    uid: int = Column(MEDIUMINT(8), primary_key=True)
    username = Column(CHAR(15), nullable=False, unique=True, server_default=text("''"))
    nickname = Column(String(30), nullable=False)
    avatar: str = Column(VARCHAR(255), nullable=False)
    groupid = Column(SMALLINT(6), nullable=False, server_default=text("'0'"))
    regdate = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
    lastvisit = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
    lastactivity = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
    lastpost = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
    dateformat = Column(CHAR(10), nullable=False, server_default=text("''"))
    timeformat = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    timeoffset = Column(CHAR(4), nullable=False, server_default=text("''"))
    newpm = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    new_notify = Column(
        SMALLINT(6), nullable=False, server_default=text("'0'"), comment="新提醒"
    )
    sign = Column(VARCHAR(255), nullable=False)


class ChiiOauthAccessToken(Base):
    __tablename__ = "chii_oauth_access_tokens"

    access_token = Column(String(40, "utf8_unicode_ci"), primary_key=True)
    client_id = Column(String(80, "utf8_unicode_ci"), nullable=False)
    user_id: str = Column(String(80, "utf8_unicode_ci"))
    expires = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )
    scope = Column(String(4000, "utf8_unicode_ci"))


t_chii_person_alias = Table(
    "chii_person_alias",
    metadata,
    Column("prsn_cat", ENUM("prsn", "crt"), nullable=False),
    Column("prsn_id", MEDIUMINT(9), nullable=False, index=True),
    Column("alias_name", String(255, "utf8_unicode_ci"), nullable=False),
    Column("alias_type", TINYINT(4), nullable=False),
    Column("alias_key", String(10, "utf8_unicode_ci"), nullable=False),
    Index("prsn_cat", "prsn_cat", "prsn_id"),
)


class ChiiPersonCollect(Base):
    __tablename__ = "chii_person_collects"
    __table_args__ = (
        Index("prsn_clt_cat", "prsn_clt_cat", "prsn_clt_mid"),
        {"comment": "人物收藏"},
    )

    prsn_clt_id = Column(MEDIUMINT(8), primary_key=True)
    prsn_clt_cat = Column(Enum("prsn", "crt"), nullable=False)
    prsn_clt_mid = Column(MEDIUMINT(8), nullable=False, index=True)
    prsn_clt_uid = Column(MEDIUMINT(8), nullable=False, index=True)
    prsn_clt_dateline = Column(INTEGER(10), nullable=False)


class ChiiPersonCsIndex(Base):
    __tablename__ = "chii_person_cs_index"
    __table_args__ = {"comment": "subjects' credits/creator & staff (c&s)index"}

    prsn_type = Column(ENUM("prsn", "crt"), primary_key=True, nullable=False)
    prsn_id = Column(
        MEDIUMINT(9),
        primary_key=True,
        nullable=False,
        index=True,
    )
    prsn_position: int = Column(
        SMALLINT(5), primary_key=True, nullable=False, index=True, comment="监督，原案，脚本,.."
    )
    subject_id = Column(
        MEDIUMINT(9),
        primary_key=True,
        nullable=False,
        index=True,
    )
    subject_type_id: int = Column(TINYINT(4), nullable=False, index=True)
    summary = Column(MEDIUMTEXT, nullable=False)
    prsn_appear_eps = Column(MEDIUMTEXT, nullable=False, comment="可选，人物参与的章节")


class ChiiPersonField(Base):
    __tablename__ = "chii_person_fields"
    __table_args__ = {"extend_existing": True}

    prsn_id = Column(INTEGER(8), primary_key=True, nullable=False, index=True)
    prsn_cat = Column(ENUM("prsn", "crt"), nullable=False)
    gender = Column(TINYINT(4), nullable=False)
    bloodtype = Column(TINYINT(4), nullable=False)
    birth_year = Column(YEAR(4), nullable=False)
    birth_mon = Column(TINYINT(2), nullable=False)
    birth_day = Column(TINYINT(2), nullable=False)
    __mapper_args__ = {"polymorphic_on": prsn_cat, "polymorphic_identity": "prsn"}


class ChiiCharacterField(ChiiPersonField):
    __mapper_args__ = {"polymorphic_identity": "crt"}


t_chii_person_relationship = Table(
    "chii_person_relationship",
    metadata,
    Column("prsn_type", ENUM("prsn", "crt"), nullable=False),
    Column("prsn_id", MEDIUMINT(9), nullable=False),
    Column("relat_prsn_type", ENUM("prsn", "crt"), nullable=False),
    Column("relat_prsn_id", MEDIUMINT(9), nullable=False),
    Column("relat_type", SMALLINT(6), nullable=False, comment="任职于，从属,聘用,嫁给，"),
    Index("relat_prsn_type", "relat_prsn_type", "relat_prsn_id"),
    Index("prsn_type", "prsn_type", "prsn_id"),
)


class ChiiPerson(Base):
    __tablename__ = "chii_persons"
    __table_args__ = {"comment": "（现实）人物表"}

    prsn_id = Column(MEDIUMINT(8), primary_key=True)
    prsn_name = Column(String(255, "utf8_unicode_ci"), nullable=False)
    prsn_type = Column(TINYINT(4), nullable=False, index=True, comment="个人，公司，组合")
    prsn_infobox: str = Column(MEDIUMTEXT, nullable=False)
    prsn_producer = Column(TINYINT(1), nullable=False, index=True)
    prsn_mangaka = Column(TINYINT(1), nullable=False, index=True)
    prsn_artist = Column(TINYINT(1), nullable=False, index=True)
    prsn_seiyu = Column(TINYINT(1), nullable=False, index=True)
    prsn_writer = Column(
        TINYINT(4), nullable=False, index=True, server_default=text("'0'"), comment="作家"
    )
    prsn_illustrator = Column(
        TINYINT(4), nullable=False, index=True, server_default=text("'0'"), comment="绘师"
    )
    prsn_actor = Column(TINYINT(1), nullable=False, index=True, comment="演员")
    prsn_summary: str = Column(MEDIUMTEXT, nullable=False)
    prsn_img = Column(String(255, "utf8_unicode_ci"), nullable=False)
    prsn_img_anidb = Column(VARCHAR(255), nullable=False)
    prsn_comment = Column(MEDIUMINT(9), nullable=False)
    prsn_collects = Column(MEDIUMINT(8), nullable=False)
    prsn_dateline = Column(INTEGER(10), nullable=False)
    prsn_lastpost = Column(INTEGER(11), nullable=False)
    prsn_lock = Column(TINYINT(4), nullable=False, index=True)
    prsn_anidb_id = Column(MEDIUMINT(8), nullable=False)
    prsn_ban = Column(
        TINYINT(3), nullable=False, index=True, server_default=text("'0'")
    )
    prsn_redirect = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
    prsn_nsfw = Column(TINYINT(1), nullable=False)


class ChiiRevHistory(Base):
    __tablename__ = "chii_rev_history"
    __table_args__ = (
        Index("rev_crt_id", "rev_type", "rev_mid"),
        Index("rev_id", "rev_id", "rev_type", "rev_creator"),
    )

    rev_id = Column(MEDIUMINT(8), primary_key=True)
    rev_type = Column(TINYINT(3), nullable=False, comment="条目，角色，人物")
    rev_mid = Column(MEDIUMINT(8), nullable=False, comment="对应条目，人物的ID")
    rev_text_id = Column(MEDIUMINT(9), nullable=False)
    rev_dateline = Column(INTEGER(10), nullable=False)
    rev_creator = Column(MEDIUMINT(8), nullable=False, index=True)
    rev_edit_summary = Column(String(200, "utf8_unicode_ci"), nullable=False)


class GzipPHPSerializedBlob(MEDIUMBLOB):
    def bind_processor(self, dialect):
        raise NotImplementedError("write to db is not supported now")

    @staticmethod
    def load_array(d: List[Tuple[Union[int, str], Any]]):
        for i, (k, v) in enumerate(d):
            if type(k) == int:
                d[i] = (str(k), v)
        return dict(d)

    @staticmethod
    def loads(b: bytes):
        return phpseralize.loads(
            zlib.decompress(b, -zlib.MAX_WBITS),
            array_hook=GzipPHPSerializedBlob.load_array,
        )

    def result_processor(self, dialect, coltype):
        loads = self.loads

        def process(value):
            if value is None:
                return None
            return loads(value)

        return process

    def compare_values(self, x, y):
        if self.comparator:
            return self.comparator(x, y)
        return x == y


class ChiiRevText(Base):
    __tablename__ = "chii_rev_text"

    rev_text_id = Column(MEDIUMINT(9), primary_key=True)
    rev_text = Column(GzipPHPSerializedBlob, nullable=False)


t_chii_subject_alias = Table(
    "chii_subject_alias",
    metadata,
    Column("subject_id", INTEGER(10), nullable=False, index=True),
    Column("alias_name", String(255), nullable=False),
    Column(
        "subject_type_id",
        TINYINT(3),
        nullable=False,
        server_default=text("'0'"),
        comment="所属条目的类型",
    ),
    Column(
        "alias_type",
        TINYINT(3),
        nullable=False,
        server_default=text("'0'"),
        comment="是别名还是条目名",
    ),
    Column("alias_key", VARCHAR(10), nullable=False),
)


class ChiiSubjectField(Base):
    __tablename__ = "chii_subject_fields"
    __table_args__ = (
        Index("query_date", "field_sid", "field_date"),
        Index("field_year_mon", "field_year", "field_mon"),
    )

    field_sid = Column(MEDIUMINT(8), primary_key=True)
    field_tid = Column(
        SMALLINT(6), nullable=False, index=True, server_default=text("'0'")
    )
    field_tags = Column(MEDIUMTEXT, nullable=False)
    field_rate_1 = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"))
    field_rate_2 = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"))
    field_rate_3 = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"))
    field_rate_4 = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"))
    field_rate_5 = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"))
    field_rate_6 = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"))
    field_rate_7 = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"))
    field_rate_8 = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"))
    field_rate_9 = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"))
    field_rate_10 = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"))
    field_airtime = Column(TINYINT(1), nullable=False, index=True)
    field_rank = Column(
        INTEGER(10), nullable=False, index=True, server_default=text("'0'")
    )
    field_year = Column(YEAR(4), nullable=False, index=True, comment="放送年份")
    field_mon = Column(TINYINT(2), nullable=False, comment="放送月份")
    field_week_day = Column(TINYINT(1), nullable=False, comment="放送日(星期X)")
    # 对于默认的零值 '0000-00-00' 会被解析成字符串。
    # 非零值会被处理成 `datetime.date`
    field_date = Column(Date, nullable=False, index=True, comment="放送日期")
    field_redirect = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"))

    def rating(self):
        scores = self.scores()
        total = 0
        total_count = 0
        for key, value in scores.items():
            total += int(key) * value
            total_count += value
        if total_count != 0:
            score = round(total / total_count, 1)
        else:
            score = 0

        return {
            "rank": self.field_rank,
            "score": score,
            "count": scores,
            "total": total_count,
        }

    def scores(self):
        return {
            "1": self.field_rate_1,
            "2": self.field_rate_2,
            "3": self.field_rate_3,
            "4": self.field_rate_4,
            "5": self.field_rate_5,
            "6": self.field_rate_6,
            "7": self.field_rate_7,
            "8": self.field_rate_8,
            "9": self.field_rate_9,
            "10": self.field_rate_10,
        }

    def tags(self) -> List[dict]:
        if not self.field_tags:
            return []

        # defaults to utf-8
        tags_deserialized = dict_to_list(phpseralize.loads(self.field_tags.encode()))

        return [
            {"name": tag["tag_name"], "count": tag["result"]}
            for tag in tags_deserialized
            if tag["tag_name"] is not None  # remove tags like { "tag_name": None }
        ]


class ChiiSubjectRelations(Base):
    """
    这个表带有 comment，也没有主键，所以生成器用的是 `Table` 而不是现在的class。
    """

    __tablename__ = "chii_subject_relations"
    __table_args__ = (
        Index(
            "rlt_relation_type",
            "rlt_relation_type",
            "rlt_subject_id",
            "rlt_related_subject_id",
        ),
        Index(
            "rlt_subject_id",
            "rlt_subject_id",
            "rlt_related_subject_id",
            "rlt_vice_versa",
            unique=True,
        ),
        Index(
            "rlt_related_subject_type_id", "rlt_related_subject_type_id", "rlt_order"
        ),
    )
    rlt_subject_id = Column(
        "rlt_subject_id",
        MEDIUMINT(8),
        nullable=False,
        comment="关联主 ID",
    )
    rlt_subject_type_id = Column(
        "rlt_subject_type_id", TINYINT(3), nullable=False, index=True
    )
    rlt_relation_type: int = Column(
        "rlt_relation_type", SMALLINT(5), nullable=False, comment="关联类型"
    )
    rlt_related_subject_id = Column(
        "rlt_related_subject_id",
        MEDIUMINT(8),
        nullable=False,
        comment="关联目标 ID",
    )
    rlt_related_subject_type_id: int = Column(
        "rlt_related_subject_type_id", TINYINT(3), nullable=False, comment="关联目标类型"
    )
    rlt_vice_versa = Column("rlt_vice_versa", TINYINT(1), nullable=False)
    rlt_order = Column("rlt_order", TINYINT(3), nullable=False, comment="关联排序")

    __mapper_args__ = {
        "primary_key": [rlt_subject_id, rlt_related_subject_id, rlt_vice_versa]
    }


class ChiiSubjectRevision(Base):
    __tablename__ = "chii_subject_revisions"
    __table_args__ = (
        Index("rev_subject_id", "rev_subject_id", "rev_creator"),
        Index("rev_creator", "rev_creator", "rev_id"),
    )

    rev_id = Column(MEDIUMINT(8), primary_key=True)
    rev_type = Column(
        TINYINT(3),
        nullable=False,
        index=True,
        server_default=text("'1'"),
        comment="修订类型",
    )
    rev_subject_id = Column(MEDIUMINT(8), nullable=False)
    rev_type_id = Column(SMALLINT(6), nullable=False, server_default=text("'0'"))
    rev_creator = Column(MEDIUMINT(8), nullable=False)
    rev_dateline = Column(
        INTEGER(10), nullable=False, index=True, server_default=text("'0'")
    )
    rev_name = Column(String(80), nullable=False)
    rev_name_cn = Column(String(80), nullable=False)
    rev_field_infobox = Column(MEDIUMTEXT, nullable=False)
    rev_field_summary = Column(MEDIUMTEXT, nullable=False)
    rev_vote_field = Column(MEDIUMTEXT, nullable=False)
    rev_field_eps = Column(MEDIUMINT(8), nullable=False)
    rev_edit_summary = Column(String(200), nullable=False)
    rev_platform = Column(SMALLINT(6), nullable=False)


class ChiiSubject(Base):
    __tablename__ = "chii_subjects"
    __table_args__ = (
        Index(
            "order_by_name",
            "subject_ban",
            "subject_type_id",
            "subject_series",
            "subject_platform",
            "subject_name",
        ),
        Index(
            "browser",
            "subject_ban",
            "subject_type_id",
            "subject_series",
            "subject_platform",
        ),
        Index("subject_idx_cn", "subject_idx_cn", "subject_type_id"),
    )

    subject_id = Column(MEDIUMINT(8), primary_key=True)
    subject_type_id = Column(
        SMALLINT(6), nullable=False, index=True, server_default=text("'0'")
    )
    subject_name = Column(String(80), nullable=False, index=True)
    subject_name_cn = Column(String(80), nullable=False, index=True)
    subject_uid = Column(String(20), nullable=False, comment="isbn / imdb")
    subject_creator = Column(MEDIUMINT(8), nullable=False, index=True)
    subject_dateline = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
    subject_image = Column(String(255), nullable=False)
    subject_platform = Column(
        SMALLINT(6), nullable=False, index=True, server_default=text("'0'")
    )
    field_infobox = Column(MEDIUMTEXT, nullable=False)
    field_summary = Column(MEDIUMTEXT, nullable=False, comment="summary")
    field_5 = Column(MEDIUMTEXT, nullable=False, comment="author summary")
    field_volumes = Column(
        MEDIUMINT(8), nullable=False, server_default=text("'0'"), comment="卷数"
    )
    field_eps: int = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"))
    subject_wish: int = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"))
    subject_collect: int = Column(
        MEDIUMINT(8), nullable=False, server_default=text("'0'")
    )
    subject_doing: int = Column(
        MEDIUMINT(8), nullable=False, server_default=text("'0'")
    )
    subject_on_hold: int = Column(
        MEDIUMINT(8), nullable=False, server_default=text("'0'"), comment="搁置人数"
    )
    subject_dropped: int = Column(
        MEDIUMINT(8), nullable=False, server_default=text("'0'"), comment="抛弃人数"
    )
    subject_series = Column(
        TINYINT(1), nullable=False, index=True, server_default=text("'0'")
    )
    subject_series_entry = Column(
        MEDIUMINT(8), nullable=False, index=True, server_default=text("'0'")
    )
    subject_idx_cn = Column(String(1), nullable=False)
    subject_airtime = Column(TINYINT(1), nullable=False, index=True)
    subject_nsfw = Column(TINYINT(1), nullable=False, index=True)
    subject_ban = Column(
        TINYINT(1), nullable=False, index=True, server_default=text("'0'")
    )

    @property
    def locked(self) -> bool:
        return self.subject_ban == 2

    @property
    def ban(self) -> bool:
        return self.subject_ban == 1

    @classmethod
    def with_default_value(
        cls,
        subject_id=1,
        subject_type_id=1,
        subject_platform=0,
        subject_image="",
        field_infobox="",
        field_summary="",
        subject_name="name",
        subject_name_cn="name_cn",
        subject_ban=0,
        subject_nsfw=0,
        field_volumes=0,
        field_eps=0,
        subject_wish=0,
        subject_collect=0,
        subject_doing=0,
        subject_on_hold=0,
        subject_dropped=0,
        field_redirect=0,
        field_rate_1=0,
        field_rate_2=0,
        field_rate_3=0,
        field_rate_4=0,
        field_rate_5=0,
        field_rate_6=0,
        field_rate_7=0,
        field_rate_8=0,
        field_rate_9=0,
        field_rate_10=0,
        field_rank=0,
    ):
        """a method to get a instance with all field has a default value"""
        return ChiiSubject(
            subject_id=subject_id,
            subject_type_id=subject_type_id,
            subject_platform=subject_platform,
            subject_image=subject_image,
            field_infobox=field_infobox,
            field_summary=field_summary,
            subject_name=subject_name,
            subject_name_cn=subject_name_cn,
            subject_ban=subject_ban,
            subject_nsfw=subject_nsfw,
            field_volumes=field_volumes,
            field_eps=field_eps,
            subject_wish=subject_wish,
            subject_collect=subject_collect,
            subject_doing=subject_doing,
            subject_on_hold=subject_on_hold,
            subject_dropped=subject_dropped,
            fields=ChiiSubjectField(
                field_redirect=field_redirect,
                field_rate_1=field_rate_1,
                field_rate_2=field_rate_2,
                field_rate_3=field_rate_3,
                field_rate_4=field_rate_4,
                field_rate_5=field_rate_5,
                field_rate_6=field_rate_6,
                field_rate_7=field_rate_7,
                field_rate_8=field_rate_8,
                field_rate_9=field_rate_9,
                field_rate_10=field_rate_10,
                field_rank=field_rank,
            ),
        )


class ChiiSubjectInterest(Base):
    __tablename__ = "chii_subject_interests"
    __table_args__ = (
        Index("user_collects", "interest_subject_type", "interest_uid"),
        Index(
            "tag_subject_id", "interest_subject_type", "interest_type", "interest_uid"
        ),
        Index(
            "subject_lasttouch",
            "interest_subject_id",
            "interest_private",
            "interest_lasttouch",
        ),
        Index(
            "user_collect_type",
            "interest_subject_type",
            "interest_type",
            "interest_uid",
            "interest_private",
            "interest_collect_dateline",
        ),
        Index(
            "subject_collect",
            "interest_subject_id",
            "interest_type",
            "interest_private",
            "interest_collect_dateline",
        ),
        Index(
            "subject_comment",
            "interest_subject_id",
            "interest_has_comment",
            "interest_private",
            "interest_lasttouch",
        ),
        Index("interest_id", "interest_uid", "interest_private"),
        Index(
            "user_collect_latest",
            "interest_subject_type",
            "interest_type",
            "interest_uid",
            "interest_private",
        ),
        Index(
            "top_subject",
            "interest_subject_id",
            "interest_subject_type",
            "interest_doing_dateline",
        ),
        Index(
            "subject_rate", "interest_subject_id", "interest_rate", "interest_private"
        ),
        Index("interest_type_2", "interest_type", "interest_uid"),
        Index(
            "interest_uid_2", "interest_uid", "interest_private", "interest_lasttouch"
        ),
        Index("user_interest", "interest_uid", "interest_subject_id", unique=True),
        Index("interest_subject_id", "interest_subject_id", "interest_type"),
    )

    id = Column("interest_id", INTEGER(10), primary_key=True)
    user_id = Column("interest_uid", MEDIUMINT(8), nullable=False, index=True)
    subject_id = Column("interest_subject_id", MEDIUMINT(8), nullable=False, index=True)
    subject_type = Column(
        "interest_subject_type",
        SMALLINT(6),
        nullable=False,
        index=True,
        server_default=text("'0'"),
    )
    rate = Column(
        "interest_rate",
        TINYINT(3),
        nullable=False,
        index=True,
        server_default=text("'0'"),
    )
    type = Column(
        "interest_type",
        TINYINT(1),
        nullable=False,
        index=True,
        server_default=text("'0'"),
    )
    has_comment = Column("interest_has_comment", TINYINT(1), nullable=False, default=0)
    comment = Column("interest_comment", MEDIUMTEXT, nullable=False, default="")
    tag: str = Column("interest_tag", MEDIUMTEXT, nullable=False, default="")
    ep_status = Column(
        "interest_ep_status",
        MEDIUMINT(8),
        nullable=False,
        server_default=text("'0'"),
    )
    vol_status = Column(
        "interest_vol_status",
        MEDIUMINT(8),
        nullable=False,
        comment="卷数",
        default=0,
    )
    wish_dateline = Column(
        "interest_wish_dateline", INTEGER(10), nullable=False, default=0
    )
    doing_dateline = Column(
        "interest_doing_dateline", INTEGER(10), nullable=False, default=0
    )
    collect_dateline = Column(
        "interest_collect_dateline", INTEGER(10), nullable=False, index=True, default=0
    )
    on_hold_dateline = Column(
        "interest_on_hold_dateline", INTEGER(10), nullable=False, default=0
    )
    dropped_dateline = Column(
        "interest_dropped_dateline", INTEGER(10), nullable=False, default=0
    )
    last_touch = Column(
        "interest_lasttouch",
        INTEGER(10),
        nullable=False,
        index=True,
        server_default=text("'0'"),
    )
    private = Column(
        "interest_private", TINYINT(1), nullable=False, index=True, default=0
    )


class ChiiIndex(Base):
    __tablename__ = "chii_index"
    __table_args__ = (
        Index("mid", "idx_id"),
        Index("idx_ban", "idx_ban"),
        Index("idx_type", "idx_type"),
        Index("idx_uid", "idx_uid"),
        Index("idx_collects", "idx_collects"),
    )
    idx_id = Column(MEDIUMINT(8), comment="自动id", primary_key=True, autoincrement=True)
    idx_type = Column(TINYINT(3), nullable=False, server_default=text("'0'"))
    idx_title = Column(VARCHAR(80), nullable=False, comment="标题")
    idx_desc = Column(MEDIUMTEXT, nullable=False, comment="简介")
    idx_replies = Column(
        MEDIUMINT(8), nullable=False, server_default="'0'", comment="回复数"
    )
    idx_subject_total = Column(
        MEDIUMINT(8), nullable=False, server_default="'0'", comment="内含条目总数"
    )
    idx_collects = Column(
        MEDIUMINT(8), nullable=False, server_default="'0'", comment="收藏数"
    )
    idx_stats = Column(MEDIUMTEXT, nullable=False)
    idx_dateline = Column(INTEGER(10), nullable=False, comment="创建时间")
    idx_lasttouch = Column(INTEGER(10), nullable=False)
    idx_uid = Column(MEDIUMINT(8), nullable=False, comment="创建人UID")
    idx_ban = Column(TINYINT(1), nullable=False, server_default="'0'")


class ChiiIndexCollects(Base):
    __tablename__ = "chii_index_collects"
    __table_args__ = (
        Index("idx_clt_mid", "idx_clt_mid", "idx_clt_uid"),
        {"comment": "目录收藏"},
    )
    idx_clt_id = Column(MEDIUMINT(8), primary_key=True, autoincrement=True)
    idx_clt_mid = Column(MEDIUMINT(8), nullable=False, comment="目录ID")
    idx_clt_uid = Column(MEDIUMINT(8), nullable=False, comment="用户UID")
    idx_clt_dateline = Column(INTEGER(10), nullable=False)


class ChiiIndexComments(Base):
    __tablename__ = "chii_index_comments"
    __table_args__ = (
        Index("idx_pst_mid", "idx_pst_mid"),
        Index("idx_pst_related", "idx_pst_related"),
        Index("idx_pst_uid", "idx_pst_uid"),
    )
    idx_pst_id = Column(MEDIUMINT(8), primary_key=True, autoincrement=True)
    idx_pst_mid = Column(MEDIUMINT(8), nullable=False)
    idx_pst_uid = Column(MEDIUMINT(8), nullable=False)
    idx_pst_related = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"))
    idx_pst_dateline = Column(INTEGER(10), nullable=False)
    idx_pst_content = Column(MEDIUMTEXT, nullable=False)


class ChiiIndexRelated(Base):
    __tablename__ = "chii_index_related"
    __table_args__ = (
        Index("idx_rlt_rid", "idx_rlt_rid", "idx_rlt_type"),
        Index("idx_rlt_sid", "idx_rlt_rid", "idx_rlt_sid"),
        Index("idx_rlt_sid_2", "idx_rlt_sid"),
        Index("index_rlt_cat", "idx_rlt_cat"),
        Index(
            "idx_order", "idx_rlt_rid", "idx_rlt_cat", "idx_rlt_order", "idx_rlt_sid"
        ),
        {"comment": "目录关联表"},
    )
    idx_rlt_id = Column(MEDIUMINT(8), primary_key=True, autoincrement=True)
    idx_rlt_cat = Column(TINYINT(3), nullable=False)
    idx_rlt_rid = Column(MEDIUMINT(8), nullable=False, comment="关联目录")
    idx_rlt_type = Column(SMALLINT(6), nullable=False, comment="关联条目类型")
    idx_rlt_sid = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"))
    idx_rlt_order = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"))
    idx_rlt_comment = Column(MEDIUMTEXT, nullable=False)
    idx_rlt_dateline = Column(INTEGER(10), nullable=False)


class ChiiTimeline(Base):
    __tablename__ = "chii_timeline"
    __table_args__ = (Index("query_tml_cat", "tml_uid", "tml_cat"),)

    if TYPE_CHECKING:

        def __init__(
            self,
            uid: int,
            cat: int,
            type: int,
            related: str,
            memo: str,
            img: str,
            batch: int,
            source: Optional[int] = None,
            replies: int = 0,
            id: Optional[int] = None,
            dateline: Optional[int] = None,
        ):
            ...

    id = Column("tml_id", INTEGER(10), primary_key=True)
    uid = Column(
        "tml_uid", MEDIUMINT(8), nullable=False, index=True, server_default=text("'0'")
    )
    cat: int = Column("tml_cat", SMALLINT(6), nullable=False, index=True)
    type: int = Column(
        "tml_type", SMALLINT(6), nullable=False, server_default=text("'0'")
    )
    related = Column(
        "tml_related", CHAR(255), nullable=False, server_default=text("'0'"), default=0
    )
    memo: str = Column("tml_memo", MEDIUMTEXT, nullable=False)
    img: str = Column("tml_img", MEDIUMTEXT, nullable=False)
    batch = Column("tml_batch", TINYINT(3), nullable=False, index=True)
    source = Column(
        "tml_source",
        TINYINT(3),
        nullable=False,
        server_default=text("'0'"),
        comment="更新来源",
        default=5,
    )
    replies = Column(
        "tml_replies", MEDIUMINT(8), nullable=False, comment="回复数", default=0
    )
    dateline: int = Column(
        "tml_dateline",
        INTEGER(10),
        nullable=False,
        server_default=text("'0'"),
        default=lambda: int(datetime.datetime.now().timestamp()),
    )


class ChiiUsergroup(Base):
    __tablename__ = "chii_usergroup"

    usr_grp_id = Column(MEDIUMINT(8), primary_key=True)
    usr_grp_name = Column(VARCHAR(255), nullable=False)
    usr_grp_perm = Column(MEDIUMTEXT, nullable=False)
    usr_grp_dateline = Column(INTEGER(10), nullable=False)
