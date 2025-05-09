PGDMP          
        
    |            quanlykhachsan    16.4    16.4 .               0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    16755    quanlykhachsan    DATABASE     �   CREATE DATABASE quanlykhachsan WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_United States.1252';
    DROP DATABASE quanlykhachsan;
                postgres    false            �            1259    16775    datphong    TABLE     �   CREATE TABLE public.datphong (
    iddatphong integer NOT NULL,
    idkhachhang integer,
    idphong integer,
    ngaynhanphong date,
    ngaytraphong date
);
    DROP TABLE public.datphong;
       public         heap    postgres    false            �            1259    16774    datphong_iddatphong_seq    SEQUENCE     �   CREATE SEQUENCE public.datphong_iddatphong_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.datphong_iddatphong_seq;
       public          postgres    false    220                       0    0    datphong_iddatphong_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.datphong_iddatphong_seq OWNED BY public.datphong.iddatphong;
          public          postgres    false    219            �            1259    16792    hoadon    TABLE     �   CREATE TABLE public.hoadon (
    idhoadon integer NOT NULL,
    iddatphong integer,
    tongtien numeric(12,2),
    ngaythanhtoan date
);
    DROP TABLE public.hoadon;
       public         heap    postgres    false            �            1259    16791    hoadon_idhoadon_seq    SEQUENCE     �   CREATE SEQUENCE public.hoadon_idhoadon_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.hoadon_idhoadon_seq;
       public          postgres    false    222                       0    0    hoadon_idhoadon_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.hoadon_idhoadon_seq OWNED BY public.hoadon.idhoadon;
          public          postgres    false    221            �            1259    16757 	   khachhang    TABLE     �   CREATE TABLE public.khachhang (
    id integer NOT NULL,
    ten text,
    sodienthoai text,
    email text,
    cmnd_hochieu text,
    matkhau text NOT NULL,
    vaitro character varying(50) DEFAULT 'customer'::character varying
);
    DROP TABLE public.khachhang;
       public         heap    postgres    false            �            1259    16756    khachhang_id_seq    SEQUENCE     �   CREATE SEQUENCE public.khachhang_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.khachhang_id_seq;
       public          postgres    false    216                       0    0    khachhang_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.khachhang_id_seq OWNED BY public.khachhang.id;
          public          postgres    false    215            �            1259    16804    lichsuluutru    TABLE     �   CREATE TABLE public.lichsuluutru (
    idlichsu integer NOT NULL,
    idkhachhang integer,
    idphong integer,
    ngayvao date,
    ngayra date
);
     DROP TABLE public.lichsuluutru;
       public         heap    postgres    false            �            1259    16803    lichsuluutru_idlichsu_seq    SEQUENCE     �   CREATE SEQUENCE public.lichsuluutru_idlichsu_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public.lichsuluutru_idlichsu_seq;
       public          postgres    false    224                       0    0    lichsuluutru_idlichsu_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE public.lichsuluutru_idlichsu_seq OWNED BY public.lichsuluutru.idlichsu;
          public          postgres    false    223            �            1259    16766    phong    TABLE     �   CREATE TABLE public.phong (
    idphong integer NOT NULL,
    soluonggiuong integer,
    tiennghi text,
    gia numeric(12,2),
    tinhtrang text
);
    DROP TABLE public.phong;
       public         heap    postgres    false            �            1259    16765    phong_idphong_seq    SEQUENCE     �   CREATE SEQUENCE public.phong_idphong_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.phong_idphong_seq;
       public          postgres    false    218                       0    0    phong_idphong_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.phong_idphong_seq OWNED BY public.phong.idphong;
          public          postgres    false    217            b           2604    16778    datphong iddatphong    DEFAULT     z   ALTER TABLE ONLY public.datphong ALTER COLUMN iddatphong SET DEFAULT nextval('public.datphong_iddatphong_seq'::regclass);
 B   ALTER TABLE public.datphong ALTER COLUMN iddatphong DROP DEFAULT;
       public          postgres    false    220    219    220            c           2604    16795    hoadon idhoadon    DEFAULT     r   ALTER TABLE ONLY public.hoadon ALTER COLUMN idhoadon SET DEFAULT nextval('public.hoadon_idhoadon_seq'::regclass);
 >   ALTER TABLE public.hoadon ALTER COLUMN idhoadon DROP DEFAULT;
       public          postgres    false    222    221    222            _           2604    16760    khachhang id    DEFAULT     l   ALTER TABLE ONLY public.khachhang ALTER COLUMN id SET DEFAULT nextval('public.khachhang_id_seq'::regclass);
 ;   ALTER TABLE public.khachhang ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    215    216    216            d           2604    16807    lichsuluutru idlichsu    DEFAULT     ~   ALTER TABLE ONLY public.lichsuluutru ALTER COLUMN idlichsu SET DEFAULT nextval('public.lichsuluutru_idlichsu_seq'::regclass);
 D   ALTER TABLE public.lichsuluutru ALTER COLUMN idlichsu DROP DEFAULT;
       public          postgres    false    223    224    224            a           2604    16769    phong idphong    DEFAULT     n   ALTER TABLE ONLY public.phong ALTER COLUMN idphong SET DEFAULT nextval('public.phong_idphong_seq'::regclass);
 <   ALTER TABLE public.phong ALTER COLUMN idphong DROP DEFAULT;
       public          postgres    false    217    218    218                      0    16775    datphong 
   TABLE DATA           a   COPY public.datphong (iddatphong, idkhachhang, idphong, ngaynhanphong, ngaytraphong) FROM stdin;
    public          postgres    false    220    5                 0    16792    hoadon 
   TABLE DATA           O   COPY public.hoadon (idhoadon, iddatphong, tongtien, ngaythanhtoan) FROM stdin;
    public          postgres    false    222   �5                 0    16757 	   khachhang 
   TABLE DATA           _   COPY public.khachhang (id, ten, sodienthoai, email, cmnd_hochieu, matkhau, vaitro) FROM stdin;
    public          postgres    false    216   �5                 0    16804    lichsuluutru 
   TABLE DATA           W   COPY public.lichsuluutru (idlichsu, idkhachhang, idphong, ngayvao, ngayra) FROM stdin;
    public          postgres    false    224   7       
          0    16766    phong 
   TABLE DATA           Q   COPY public.phong (idphong, soluonggiuong, tiennghi, gia, tinhtrang) FROM stdin;
    public          postgres    false    218   a7                  0    0    datphong_iddatphong_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.datphong_iddatphong_seq', 14, true);
          public          postgres    false    219                       0    0    hoadon_idhoadon_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.hoadon_idhoadon_seq', 12, true);
          public          postgres    false    221                       0    0    khachhang_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.khachhang_id_seq', 19, true);
          public          postgres    false    215                       0    0    lichsuluutru_idlichsu_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.lichsuluutru_idlichsu_seq', 3, true);
          public          postgres    false    223                        0    0    phong_idphong_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.phong_idphong_seq', 1, false);
          public          postgres    false    217            n           2606    16780    datphong datphong_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.datphong
    ADD CONSTRAINT datphong_pkey PRIMARY KEY (iddatphong);
 @   ALTER TABLE ONLY public.datphong DROP CONSTRAINT datphong_pkey;
       public            postgres    false    220            p           2606    16797    hoadon hoadon_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.hoadon
    ADD CONSTRAINT hoadon_pkey PRIMARY KEY (idhoadon);
 <   ALTER TABLE ONLY public.hoadon DROP CONSTRAINT hoadon_pkey;
       public            postgres    false    222            f           2606    16764    khachhang khachhang_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.khachhang
    ADD CONSTRAINT khachhang_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.khachhang DROP CONSTRAINT khachhang_pkey;
       public            postgres    false    216            r           2606    16809    lichsuluutru lichsuluutru_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.lichsuluutru
    ADD CONSTRAINT lichsuluutru_pkey PRIMARY KEY (idlichsu);
 H   ALTER TABLE ONLY public.lichsuluutru DROP CONSTRAINT lichsuluutru_pkey;
       public            postgres    false    224            l           2606    16773    phong phong_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.phong
    ADD CONSTRAINT phong_pkey PRIMARY KEY (idphong);
 :   ALTER TABLE ONLY public.phong DROP CONSTRAINT phong_pkey;
       public            postgres    false    218            h           2606    16832    khachhang so_dien_thoai_unique 
   CONSTRAINT     `   ALTER TABLE ONLY public.khachhang
    ADD CONSTRAINT so_dien_thoai_unique UNIQUE (sodienthoai);
 H   ALTER TABLE ONLY public.khachhang DROP CONSTRAINT so_dien_thoai_unique;
       public            postgres    false    216            j           2606    16830    khachhang unique_so_dien_thoai 
   CONSTRAINT     `   ALTER TABLE ONLY public.khachhang
    ADD CONSTRAINT unique_so_dien_thoai UNIQUE (sodienthoai);
 H   ALTER TABLE ONLY public.khachhang DROP CONSTRAINT unique_so_dien_thoai;
       public            postgres    false    216            s           2606    16781 "   datphong datphong_idkhachhang_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.datphong
    ADD CONSTRAINT datphong_idkhachhang_fkey FOREIGN KEY (idkhachhang) REFERENCES public.khachhang(id) ON DELETE CASCADE;
 L   ALTER TABLE ONLY public.datphong DROP CONSTRAINT datphong_idkhachhang_fkey;
       public          postgres    false    220    216    4710            t           2606    16786    datphong datphong_idphong_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.datphong
    ADD CONSTRAINT datphong_idphong_fkey FOREIGN KEY (idphong) REFERENCES public.phong(idphong) ON DELETE CASCADE;
 H   ALTER TABLE ONLY public.datphong DROP CONSTRAINT datphong_idphong_fkey;
       public          postgres    false    220    4716    218            u           2606    16798    hoadon hoadon_iddatphong_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.hoadon
    ADD CONSTRAINT hoadon_iddatphong_fkey FOREIGN KEY (iddatphong) REFERENCES public.datphong(iddatphong) ON DELETE CASCADE;
 G   ALTER TABLE ONLY public.hoadon DROP CONSTRAINT hoadon_iddatphong_fkey;
       public          postgres    false    4718    220    222            v           2606    16810 *   lichsuluutru lichsuluutru_idkhachhang_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.lichsuluutru
    ADD CONSTRAINT lichsuluutru_idkhachhang_fkey FOREIGN KEY (idkhachhang) REFERENCES public.khachhang(id) ON DELETE CASCADE;
 T   ALTER TABLE ONLY public.lichsuluutru DROP CONSTRAINT lichsuluutru_idkhachhang_fkey;
       public          postgres    false    4710    224    216            w           2606    16815 &   lichsuluutru lichsuluutru_idphong_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.lichsuluutru
    ADD CONSTRAINT lichsuluutru_idphong_fkey FOREIGN KEY (idphong) REFERENCES public.phong(idphong) ON DELETE CASCADE;
 P   ALTER TABLE ONLY public.lichsuluutru DROP CONSTRAINT lichsuluutru_idphong_fkey;
       public          postgres    false    4716    218    224               \   x�]��� ��.Tq(����h*��|>wa���y�Z�/^1&��#��#Taޒ/Ӂ8c\,�2}}��g��?w?����sӌ���G&         K   x�u���0Cѳ�K�84@va�9������,$��M3��Ұ����J
^I�������'�lGm�=��\`)�         "  x���=N1�k�)r�hlϏ݅��4���D�n!׉�E$��$7��f�(AW���{3�̟oo�L�^�"3���g�Nכi��Ht�A��u��%D�i����X1����<��&��ӡ]M���7P�H��Y���u�/�*�0Đ�@�dd�R�.:��$V],R"S.J�"$�1�%���	-��.��Jd���vC�JLh%c`�%�XA�_J�EAr�!.RD�h�#3�ݶ���Ld����Fwix��*s�W����~��� Ѵ���{�����d��žL���4l��         8   x�3�4�440�4202�54�50���2�4�
�Å�L.cti#��=... (�}      
   �   x�34��4��t��Q	�Q�=��R!�ᮅy�� �g`�YR�p�ļt.CCTraW�d�e�&%q�b�gD�>c2����ϔL}fd�3'S���,��L%��3�;��ud���
G&>ܵ��Ød&$�0%Y��:�ґ����p�|�zRr-0ݐ�=... ��a     